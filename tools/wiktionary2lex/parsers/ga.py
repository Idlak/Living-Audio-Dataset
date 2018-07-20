#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Copyright 2018 Cereproc Ltd. (author: Caoimhín Laoide-Kemp)
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

# NOTE: This parser only extracts Irish words
# NOTE: The Irish Wiktionary contains no accent data, so this parser returns
#       None for all accents

import sys
import time
import re
import pickle
from lxml import etree as ET

import parser_lib

def extract_entries(wiktionary_xml):
    if __debug__:
        print "Starting parse"
    tree = ET.parse(wiktionary_xml)
    if __debug__:
        print "Finished parse"
    root = tree.getroot()

    # Various patterns for matching the data we need to extract
    language_pattern = re.compile("{{-ga-}}|{{t\|ga}}")
    pronunciation_pattern = re.compile("\*IPA: {{IPA\|/(.+?)/}}")
    POS_categories = {"noun":"Noun","ainm":"Noun","ainmd":"Noun",
                      "propn":"Noun","fainm":"Noun","nounf":"Noun",
                      "aid":"Adjective","adj":"Adjective","art":"Adjective",
                      "part":"Adjective","aidsheal":"Adjective",
                      "faid":"Adjective","dobh":"Adverb","briath":"Verb",
                      "fbriath":"Verb","conj":"Conjunction","cón":"Conjuction",
                      "prep":"Preposition","rfh":"Preposition","num":"Number",
                      "uimh":"Number","forc":"Pronoun","for":"Pronoun",
                      "int":"Interjection"}

    output_data = []
    entry_POS = set()
    language = "Irish"

    for index, entry in enumerate(root):
        word = entry[0].text

        # The field containing the actual text for the article in entry[3]
        for subentry in entry[3]:

            # Matches the subentry containing the data we need
            if subentry.tag=='{http://www.mediawiki.org/xml/export-0.10/}text':

                # Some entries have empty text fields that break the parser
                if subentry.text is None:
                    break

                else:
                    for language_match in re.finditer(
                            language_pattern,subentry.text):

                        # Store the parts of speech that are mentioned
                        entry_POS.clear()
                        for key,value in POS_categories.items():
                            if "{{-" + key + "-|ga}}" in \
                                    subentry.text.encode("utf-8"):
                                entry_POS.add(value)

                        # State variable used to ensure that an entry 
                        # is added even if no accent data is available
                        no_pronunciation_data = 1

                        for pronunciation_match in re.finditer(
                                pronunciation_pattern,subentry.text):
                            no_pronunciation_data = 0
                            output_data.extend(parser_lib.make_entries(
                                    word,
                                    pronunciation_match.group(1),
                                    entry_POS,
                                    language,
                                    None,
                                    None))

                        if no_pronunciation_data:
                            output_data.extend(parser_lib.make_entries(
                                    word,
                                    None,
                                    entry_POS,
                                    language,
                                    None,
                                    None))
    return output_data

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')

    wiktionary_xml = sys.argv[1]

    output = extract_entries(wiktionary_xml)
    
    if __debug__:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        output_filename = "output/output_" + timestr + ".txt"
        output_file = open(output_filename,'wb')
        pickle.dump(output,output_file)
        parser_lib.print_output(output)
