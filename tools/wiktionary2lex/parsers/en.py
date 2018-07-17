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
    language_pattern = re.compile("==([^=]+?)==\n")
    pronunciation_pattern = re.compile("(.*?{{.*?\/(.*?)\/.*?}}.*)")
    # This one matches the set of braces that contains the accent data
    accent_set_pattern = re.compile("({{a.*?}})")
    accent_pattern = re.compile("\|(.*?)(?=[|}])")
    POS_categories = {"Noun","Pronoun","Verb","Adjective",
                      "Adverb","Conjunction","Preposition","Interjection",
                      "Number"}

    output_data = []
    entry_POS = []

    for index, entry in enumerate(root):
        word = entry[0].text

        # The field containing the actual text for the article in entry[3]
        for subentry in entry[3]:

            # Matches the subentry containing the data we need
            if subentry.tag=='{http://www.mediawiki.org/xml/export-0.10/}text':

                # Some entries have empty text fields that break the parser
                if subentry.text is None:
                    break

                for language_match in re.finditer(language_pattern,
                                                  subentry.text):
                    if __debug__:
                        print word + " has " + \
                              language_match.group(1) + " entry"
                    # Discard everything up to the name of the language
                    discard, keep = subentry.text.split(
                            "==" + language_match.group(1) + "==",1)

                    # ---- is the the marker for boundaries between languages
                    # Discard everthing after it if it exists
                    if "----" in keep:
                        keep, discard = keep.split("----",1)
                
                    # Store the parts of speech that are mentioned in headings
                    del entry_POS[:]
                    for POS in POS_categories:
                        if "===" + POS + "===" in keep:
                            entry_POS.append(POS)

                    # If pronunciation section exists, isolate it
                    # If not move to the next language
                    if "===Pronunciation===" in keep:
                        discard, pronunciation_section = keep.split(
                                "===Pronunciation===",1)

                        # Discard everything after the pronunciation section
                        # (The next section starts with = if it exists)
                        if "\n=" in pronunciation_section:
                            pronunciation_section, discard = \
                                    pronunciation_section.split("\n=",1)

                        # Find pronunciation data
                        for pronunciation_match in re.finditer(
                                    pronunciation_pattern,
                                    pronunciation_section):
                            if __debug__:
                                print "\tFound pronunciation " + \
                                        pronunciation_match.group(2)

                            # State variable used to ensure that an entry 
                            # is added even if no accent data is available
                            no_accent_sets = 1

                            for accent_set_match in re.finditer(
                                    accent_set_pattern,
                                    pronunciation_match.group(1)):
                                if __debug__:
                                    print "\t\tFound accent set " + \
                                            accent_set_match.group(1)

                                no_accent_sets = 0
                                
                                for accent_match in re.finditer(
                                        accent_pattern,
                                        accent_set_match.group(1)):
                                    if __debug__:
                                        print "\t\t\tFound accent " + \
                                                accent_match.group(1)

                                    add_to_output(
                                            output_data,
                                            word,
                                            pronunciation_match.group(2),
                                            entry_POS,
                                            language_match.group(1),
                                            accent_match.group(1),
                                            None)

                            if no_accent_sets:
                                add_to_output(
                                        output_data,
                                        word,
                                        pronunciation_match.group(2),
                                        entry_POS,
                                        language_match.group(1),
                                        None,
                                        None)
                    else:
                        add_to_output(
                                output_data,
                                word,
                                None,
                                entry_POS,
                                language_match.group(1),
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
        output.append({
                "word":word, "pron":pronunciation, 
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
