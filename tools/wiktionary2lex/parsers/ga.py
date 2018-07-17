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

from lxml import etree as ET
import sys
import time
import re
import pickle

def data_stripping(xml):
    if __debug__:
        print "Starting parse"
    tree = ET.parse(xml)
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
                            if "{{-" + key + "-|ga}}" in subentry.text:
                                entry_POS.add(value)

                        # State variable used to ensure that an entry 
                        # is added even if no accent data is available
                        no_pronunciation_data = 1

                        for pronunciation_match in re.finditer(
                                pronunciation_pattern,subentry.text):
                            no_pronunciation_data = 0
                            add_to_output(
                                    output_data,
                                    word,
                                    pronunciation_match.group(1),
                                    entry_POS,
                                    language,
                                    None,
                                    None)

                        if no_pronunciation_data:
                            add_to_output(
                                    output_data,
                                    word,
                                    None,
                                    entry_POS,
                                    language,
                                    None,
                                    None)
    return output_data

def add_to_output(output,word,pronunciation,POS,language,accent,xsampa):
    for entry in POS:
        output.append({
                "word":word, "pron":pronunciation, 
                "POS":entry, "lang":language, 
                "accent":accent, "x-sampa":xsampa})
    
    # Adds an entry even if no part of speech data is available
    if len(POS)==0:
        output.append({"word":word, "pron":pronunciation, 
                "POS":None, "lang":language, 
                "accent":accent, "x-sampa":xsampa})

def print_output(output):
    for list_item in output:
        for key in list_item:
            if list_item[key] is None:
                print key + ":None\t",
            else:
                print key + ":" + list_item[key] + "\t",
        print "\n"

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')

    xml = sys.argv[1]

    output = data_stripping(xml)
    
    if __debug__:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        output_filename = "output/output_" + timestr + ".txt"
        output_file = open(output_filename,'wb')
        pickle.dump(output,output_file)
        print_output(output)
