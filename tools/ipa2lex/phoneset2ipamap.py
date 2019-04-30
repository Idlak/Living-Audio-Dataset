#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Cereproc Ltd. (author: Caoimhín Laoide-Kemp)
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

def import_phone_map(phoneset_xml):
    tree = ET.parse(phoneset_xml)
    root = tree.getroot()
    phone_map = {}
    for entry in root:
        if len(entry)>0:
            if entry[0].get("archiphone") == "true":
                continue
            phone_map[entry[0].get("ipa")] = entry.get("name")
    return phone_map

def import_nuclei(sylmax_xml):
    tree = ET.parse(sylmax_xml)
    root = tree.getroot()
    for component in root:
        if component.tag == "nuclei":
            nuclei = [nucleus.get("pat") for nucleus in component]
    return nuclei

def create_output(phone_map,output_file,nuclei=[],add_nuclei=False):
    root = ET.Element("ipa_mapping")
    tree = ET.ElementTree(root)
    for ipa, phone in phone_map.items():
        mapping = ET.SubElement(root, "map")
        mapping.attrib["pron"] = phone
        mapping.attrib["ipa"] = ipa
        if add_nuclei:
            if phone in nuclei:
                mapping.attrib["nucleus"] = "true"
            else:
                mapping.attrib["nucleus"] = "false"
    mapping_output = open(output_file,"wb")
    tree.write(
            mapping_output,pretty_print=True,   
            xml_declaration=True,encoding="utf-8")

def parse_arguments():
    arg_parser = argparse.ArgumentParser(
            description="Select phoneset, and output file")
    arg_parser.add_argument(
            "phoneset",
            type=str,
            help="xml file that contains the phoneset in Idlak format")
    arg_parser.add_argument(
            "sylmax",
            nargs="?",
            help="Optional xml file that contains the information about valid \
                    syllables")
    arg_parser.add_argument(
            "output",
            default="mapping.xml",
            type=str,
            help="Output file for storing the mapping")
    args = vars(arg_parser.parse_args())
    return args

if __name__ == "__main__":
    args = parse_arguments()
    phoneset_xml = args["phoneset"]
    sylmax_xml = args["sylmax"]
    output_file = args["output"]
    
    nuclei = []
    add_nuclei = False
    if sylmax_xml is not None:
        add_nuclei = True
        nuclei = import_nuclei(sylmax_xml)
    phone_map = import_phone_map(phoneset_xml)
    create_output(phone_map,output_file,nuclei,add_nuclei)
