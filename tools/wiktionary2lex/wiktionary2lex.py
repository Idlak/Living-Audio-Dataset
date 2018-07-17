#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from third_party import cxs
import imp
import sys

def ipa2xsampa(ipa_text,table):
    xsampa_text = cxs.ucipa2cxs(ipa_text,table)
    return xsampa_text

def xml2dict(language_code,xml):
    parser_module = imp.load_source("parser","parsers/" + language_code + ".py")
    output = parser_module.data_stripping(xml)
    return output

def add_xsampa_to_data(parsed_data):
    F = file('third_party/CXS.def')
    table = cxs.make_table(F)
    for entry in parsed_data:
        if entry["pron"] is not None:
            entry["x-sampa"] = ipa2xsampa(entry["pron"],table)

def print_output(output):
    for list_item in output:
        for key in list_item:
            if list_item[key] is None:
                print key + ":None\t",
            else:
                print key + ":" + list_item[key] + "\t",
        print "\n"

if __name__ == "__main__":
    language_code = sys.argv[1]
    xml = sys.argv[2]
    output = xml2dict(language_code,xml)
    add_xsampa_to_data(output)
    print_output(output)
