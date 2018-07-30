#!/usr/bin/env python3
"""
This script takes a Wikipedia dump and stores its articles in the specified Idlak database format
(github.com/idlak/idlak-resources).
"""

# TODO: limit the size of output file
# TODO: make python2 compatible

from lxml import etree
import ast
import os
import subprocess
import argparse
import logging

parser = argparse.ArgumentParser(description='Specify location for temporary file storage and of the Wikipedia dump '
                                             'and output file name to generate an xml file in Idlak structure ')
parser.add_argument('temp_folder', nargs='+', help="specify output folder name and file path")
parser.add_argument('wiki_download', nargs='+', help="specify location of Wikipedia dump file")
parser.add_argument('out_name', nargs='+', help="output name")
args = parser.parse_args()


logging.basicConfig(filename='data.log', level=logging.DEBUG)


def download_parse_wiki(out_folder, wiki_download):
    """
    Takes wiki dump and uses WikiEctract to get the clean text to return idlak-structured database file
    :param out_folder: out folder for cleaned wiki text
    :param wiki_download: wikipedia dump
    :return: dict with page title as key and text as value
    """
    wiki_dict = {}
    subprocess.run(['rm', '-R', out_folder])
    subprocess.run(['mkdir', out_folder])
    subprocess.Popen("WikiExtractor.py -o {} -b 1M --json {}".format(out_folder, wiki_download),
                           shell=True, stdout=subprocess.PIPE).stdout.read()
    rootdir = out_folder

    root = etree.Element('text_sources')
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            print(os.path.join(subdir, file))
            with open(os.path.join(subdir, file), encoding='utf-8') as infile:
                data = infile.readlines()
                logging.info(data)
                for dict in data:
                    child = etree.SubElement(root, "text_source")
                    dict = ast.literal_eval(dict)
                    child.set("id", dict["id"])
                    child.set("name", dict["title"])
                    child.set("url", dict["url"])
                    subchild = etree.SubElement(child, "text")
                    subchild.text = dict["text"]
    print(len(root.getchildren()))
    subprocess.run(['rm', '-R', out_folder])
    string = etree.tostring(root, pretty_print=True, encoding='UTF-8')
    return string


if __name__ == "__main__":
    string = download_parse_wiki(args.temp_folder[0], args.wiki_download[0])
    with open(args.out_name[0], 'w') as data_out:
        data_out.write('<?xml version="1.0"?>' + '\n')
        data_out.write(string.decode('utf8'))

