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

import argparse
import json
import lxml.etree
import os
import time
import shutil
import subprocess
import tempfile

def split_corpus(fileobj, workingdir):
    corpus = lxml.etree.parse(fileobj)
    newfiles = []
    for node in corpus.xpath('./text_source'):
        fn = os.path.join(workingdir, node.attrib['id'] + '.xml')
        fn = fn.replace(' ', '_')
        with open(fn, 'w') as fout:
            srcxml = lxml.etree.Element("doc")
            srcxml.text = node.find('./text').text
            xmlstr = lxml.etree.tostring(srcxml,
                                         pretty_print=True,
                                         xml_declaration=True,
                                         encoding='utf-8')
            fout.write(xmlstr.decode('utf-8'))
        newfiles.append(fn)
    return newfiles


def process_text(fn, fnout, idlaktxp, tpdb, lng, acc):
    subprocess.call([
        idlaktxp,
        '--general-lang='+lng,
        '--general-acc='+acc,
        '--tpdb='+tpdb,
        '--pretty',
        fn,
        fnout])


def xml2stats(fn):
    processed = lxml.etree.parse(open(fn))
    utterances = []

    for utt in processed.xpath('./utt'):
        utt_tks = []
        prons = ['sil']
        for tk in utt.xpath('./spt/tk'):
            if 'pron' in tk.attrib and tk.text:
                utt_tks.append(tk.text.strip())
                prons.extend(tk.attrib['pron'].split())
        prons.append('sil')

        utt_stats = {
            'no_tokens': len(utt_tks),
            'prompt' :  ' '.join(utt_tks),
            'phoneme_counts' : {},
            'diphone_counts' : {},
        }

        for p in prons[1:-1]:
            if p not in utt_stats['phoneme_counts']:
                utt_stats['phoneme_counts'][p] = 0
            utt_stats['phoneme_counts'][p] += 1

        diphones = map(lambda p: '{} {}'.format(p[0], p[1]), zip(prons[:-1], prons[1:]))
        for d in diphones:
            if d not in utt_stats['diphone_counts']:
                utt_stats['diphone_counts'][d] = 0
            utt_stats['diphone_counts'][d] += 1

        utterances.append(utt_stats)

    return utterances

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--language", default="en",
                        help = "language")
    parser.add_argument("-a", "--accent", default="ga",
                        help = "accent")

    parser.add_argument("-I", "--idlak-data", default= os.path.join(".", 'idlak-data'),
                        help = "'idlak-data' folder")

    parser.add_argument("--idlaktxp", default="idlaktxp",
                        help = "'idlaktxp' binary")

    parser.add_argument("--working-dir", default=None,
                        help = "working directory")

    parser.add_argument("-i", "--input", action = "append", required = True,
                        type = argparse.FileType('r'),
                        help = "input file (can be given multiple times)")

    parser.add_argument("-o", "--output", default = 'decomposed_corpus.json', type = argparse.FileType('w'),
                        help = "output file (JSON format)")
    args = parser.parse_args()

    if args.working_dir is None:
        workingdir = tempfile.mkdtemp()
    else:
        workingdir = args.working_dir

    textfiles = []
    for infile in args.input:
        textfiles += split_corpus(infile, workingdir)

    procfiles = []
    for textfn in textfiles:
        procfn = os.path.splitext(textfn)[0] + '.processed.xml'
        process_text(textfn, procfn,
                 args.idlaktxp, args.idlak_data, args.language, args.accent)
        procfiles.append(procfn)

    stats = []
    for procfn in procfiles:
        fstats = xml2stats(procfn)
        stats.append(fstats)

    json.dump({'stats' : stats}, args.output, indent=2)

    if args.working_dir is None:
        shutil.rmtree(workingdir)


if __name__ == "__main__":
    main()
