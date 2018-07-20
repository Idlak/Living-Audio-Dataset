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

import ga
import en

def get_parser(language_code):
    lookup = {
            "ga":ga,
            "en":en}
    return lookup[language_code].extract_entries

def print_output(output):
    for list_item in output:
        for key in list_item:
            if list_item[key] is None:
                print key + ":None\t",
            else:
                print key + ":" + list_item[key] + "\t",
        print "\n"

def make_entries(word,pronunciation,POS,language,accent,xsampa):
    output = []
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
    
    return output
