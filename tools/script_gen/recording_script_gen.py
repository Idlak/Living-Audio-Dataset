#!/usr/bin/env python3
#
# Copyright 2018 author: Alex Brouwer
#                Cereproc Ltd. (author: David A. Braude)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# THIS CODE IS PROVIDED *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
# WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
# MERCHANTABLITY OR NON-INFRINGEMENT.
# See the Apache 2 License for the specific language governing permissions and
# limitations under the License.

# TODO: functionality to load partial recording script

import argparse
import copy
import logging
import lxml.etree
import math
import json
import random
import re

logging.basicConfig(level = logging.INFO)

# this is a very simple approach, a GA would probably work better


_new_phone_bias = 6
_new_diphone_bias = 4

def calc_score(phoneme_counts, diphone_counts):
    score = 0
    for v in phoneme_counts.values():
        for s in range(v):
            score += math.exp(_new_phone_bias - s)
    for v in diphone_counts.values():
        for s in range(v):
            score += math.exp(_new_diphone_bias - s)
    return score

def score_prompt(prompt_stats, phoneme_counts, diphone_counts):
    p_counts = copy.copy(phoneme_counts)
    d_counts = copy.copy(diphone_counts)
    for phn in prompt_stats['phoneme_counts']:
        if phn not in p_counts:
            p_counts[phn] = 0
        p_counts[phn] += 1
    for dip in prompt_stats['diphone_counts']:
        if dip not in d_counts:
            d_counts[dip] = 0
        d_counts[dip] += 1
    return calc_score(p_counts, d_counts)


def stats2script(stats, search_width, no_utterances):
    script_with_stats = []
    _stats = copy.copy(stats)

    if search_width <= 0:
        search_width = len(_stats)
    search_width = min(len(stats), search_width)
    no_utterances = min(len(stats), no_utterances)

    phoneme_counts = {}
    diphone_counts = {}

    while len(script_with_stats) < no_utterances and len(_stats):
        search_width = min(len(_stats), search_width)
        selection = random.sample(_stats, search_width)

        max_score = score_prompt(selection[0], phoneme_counts, diphone_counts)
        prompt = selection[0]
        for p in selection[1:]:
            s = score_prompt(p, phoneme_counts, diphone_counts)
            if s > max_score:
                max_score = s
                prompt = p

        for phn in prompt['phoneme_counts']:
            if phn not in phoneme_counts:
                phoneme_counts[phn] = 0
            phoneme_counts[phn] += 1
        for dip in prompt['diphone_counts']:
            if dip not in diphone_counts:
                diphone_counts[dip] = 0
            diphone_counts[dip] += 1

        script_with_stats.append(prompt)
        _stats.remove(prompt)
        logging.info("score after {} prompts: {:.1f} ".format(
            len(script_with_stats),
            calc_score(phoneme_counts, diphone_counts)))


    script = list(map(lambda s: s['prompt'], script_with_stats))
    return script


def scrit2xml(script, genre):
    xml = lxml.etree.Element('recording_script')
    major_count = 1
    count = 1
    for prompt in script:
        fileid = lxml.etree.SubElement(xml, 'fileid')
        fileid.attrib['id'] = '{}{:04d}_{:03d}'.format(genre, major_count, count)
        count += 1
        if count == 1000:
            count = 1
            major_count += 1
        fileid.text = prompt.strip()
    return xml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--genre", default = 'z',
                        help = "genre")
    parser.add_argument("-n", "--no-utterances", default = 999, type=int,
                        help = "how many utterances")
    parser.add_argument("-s", "--search-width", default = 100, type=int,
                        help = "how many utterances to consider when finding the next one for the script (-1 means all)")

    parser.add_argument("-m", "--max-words", default = 15, type=int,
                        help = "discard utterances with more than this amount of words")


    parser.add_argument("-i", "--input", action = "append", required = True,
                        type = argparse.FileType('r'),
                        help = "input file (can be given multiple times)")

    parser.add_argument("-o", "--output", default = 'text.xml',
                        type = argparse.FileType('w'),
                        help = "output recording script")
    args = parser.parse_args()

    if len(args.genre) > 1 or not re.match(r'[a-z]', args.genre):
        parser.error('genre must be a single letter')

    stats = []
    for fin in args.input:
        fstats = json.load(fin)
        for st in fstats['stats']:
            for s in st:
                if s['prompt'] and s['no_tokens'] <= args.max_words:
                    stats.append(s)

    script = stats2script(stats, args.search_width, args.no_utterances)
    scriptxml = scrit2xml(script, args.genre)

    args.output.write(lxml.etree.tostring(scriptxml,
        pretty_print=True,
        xml_declaration=True, encoding='utf-8').decode('utf-8'))
    args.output.write('\n')

if __name__ == "__main__":
    main()
