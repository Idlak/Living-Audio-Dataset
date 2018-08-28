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

import sys
import itertools
import argparse
from lxml import etree as ET

from third_party import cxs

from parsers import parser_lib

def ipa2xsampa(ipa_text,table):
    xsampa_text = cxs.ucipa2cxs(ipa_text,table)
    return xsampa_text

def xml2dict(language_code,wiktionary_xml):
    extract_entries = parser_lib.get_parser(language_code)
    output = extract_entries(wiktionary_xml)
    return output

def add_xsampa_to_data(parsed_data):
    F = file('third_party/CXS.def')
    table = cxs.make_table(F)
    for entry in parsed_data:
        if entry["pron"] is not None:
            entry["x-sampa"] = ipa2xsampa(entry["pron"],table)

def output2lex(output,filename):
    lexicon_output = open(filename,"wb")
    lexicon = ET.Element("lexicon")
    tree = ET.ElementTree(lexicon)

    for list_item in output:
        lex_entry = ET.SubElement(lexicon,"lex")
        if list_item["pron"] is not None:
            lex_entry.attrib["ipa"]=list_item["pron"]
        if list_item["x-sampa"] is not None:
            lex_entry.attrib["x-sampa"]=list_item["x-sampa"]
        lex_entry.text=list_item["word"]

    tree.write(
            lexicon_output,pretty_print=True,   
            xml_declaration=True,encoding="utf-8")

def compare(dictionary1,dictionary2,*filters):
    for key in filters:
        if dictionary1[key] != dictionary2[key]:
            return False
    return True

def filter_list(data,*filters):
    filtered_data = [[d,True] for d in data]

    for first,second in itertools.combinations(filtered_data,2):
        if first[1] and compare(first[0],second[0],*filters):
            second[1]=False

    return [list_item[0] for list_item in filtered_data if list_item[1]]

def parse_arguments():
    arg_parser = argparse.ArgumentParser(
            description="Select parser, wiktionary dump, and output file")
    arg_parser.add_argument(
            "language code",
            default="en",
            type=str,
            help="Language code used to determine which parser to use")
    arg_parser.add_argument(
            "wiktionary xml",
            type=str,
            help="xml file containing the wiktionary dump to parse")
    arg_parser.add_argument(
            "output",
            default="lex.xml",
            type=str,
            help="Output file for storing the final lexicon")
    args = vars(arg_parser.parse_args())
    return args

if __name__ == "__main__":
    args = parse_arguments()
    language_code = args["language code"]
    wiktionary_xml = args["wiktionary xml"]
    output_lexicon = args["output"]

    output = xml2dict(language_code,wiktionary_xml)
    add_xsampa_to_data(output)
    parser_lib.print_output(output)
    filtered_output=filter_list(output,"x-sampa","word")
    output2lex(filtered_output,output_lexicon)
