#!/usr/bin/env python3
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

import argparse
from lxml import etree as ET

def converter(ipa_text,phone_map,sorted_ipa):
    pron_text = []
    while len(ipa_text) > 0:
        if ipa_text[0] == " ":
            ipa_text = ipa_text[1:]
        else:
            match = False
            for ipa in sorted_ipa:
                if ipa_text.startswith(ipa):
                    pron_text.append(phone_map[ipa])
                    ipa_text = ipa_text[len(ipa):]
                    match = True
                    break
            if match == False:
                print("WARNING: Could not match symbol",ipa_text[:1])
                ipa_text = ipa_text[1:]
    return ' '.join(pron_text)

def convert_lexicon(lex_xml,phone_map,sorted_ipa):
    tree = ET.parse(lex_xml)
    root = tree.getroot()
    for entry in root:
        entry.attrib["pron"] = converter(entry.get("ipa"),phone_map,sorted_ipa)
        entry.attrib["provenance"] = "IPA conversion"
    return tree

def import_phone_map(mapping_xml):
    tree = ET.parse(mapping_xml)
    root = tree.getroot()
    phone_map = {}
    for entry in root:
        phone_map[entry.get("ipa")] = entry.get("pron")
    return phone_map

def ipa_by_length(phone_map):
    sorted_ipa = []
    for ipa in sorted(phone_map, key=len, reverse=True):
        sorted_ipa.append(ipa)
    return sorted_ipa

def output_to_file(xml_tree,output_file):
    lexicon_output = open(output_file,"wb")
    tree.write(
            lexicon_output,pretty_print=True,   
            xml_declaration=True,encoding="utf-8")

def parse_arguments():
    arg_parser = argparse.ArgumentParser(
            description="Select phoneset, lexicon, and output file")
    arg_parser.add_argument(
            "mapping",
            type=str,
            help="xml file that contains the mapping from IPA -> phones")
    arg_parser.add_argument(
            "lexicon",
            type=str,
            help="xml file containing lexicon with IPA to convert")
    arg_parser.add_argument(
            "output",
            default="lex.xml",
            type=str,
            help="Output file for storing the final lexicon")
    args = vars(arg_parser.parse_args())
    return args

if __name__ == "__main__":
    args = parse_arguments()
    mapping_xml = args["mapping"]
    lex_xml = args["lexicon"]
    output_file = args["output"]

    phone_map = import_phone_map(mapping_xml)
    sorted_ipa = ipa_by_length(phone_map)
    tree = convert_lexicon(lex_xml,phone_map,sorted_ipa)
    output_to_file(tree,output_file)
