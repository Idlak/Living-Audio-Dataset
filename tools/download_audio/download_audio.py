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
import urllib.request
import urllib.parse

def download_audio(url):
    print("Downloading audio from " + url)
    split = urllib.parse.urlsplit(url)
    filename = split.path.split("/")[-1]
    urllib.request.urlretrieve(url,filename)
    return

def get_url(lang,acc,spk):
    filepath = "../../" + lang + "/" + acc + "/" +spk + "/audiourl"
    f = open(filepath,"r")
    return f.read().rstrip()

def parse_arguments():
    arg_parser = argparse.ArgumentParser(
            description="Select language, accent and speaker")
    arg_parser.add_argument(
            "language",
            type=str,
            help="Two-letter language code")
    arg_parser.add_argument(
            "accent",
            type=str,
            help="Two-letter accent code")
    arg_parser.add_argument(
            "speaker",
            type=str,
            help="Three-letter speaker code")
    args = vars(arg_parser.parse_args())
    return args

if __name__ == "__main__":
    args = parse_arguments()
    lang = args["language"]
    acc = args["accent"]
    spk = args["speaker"]

    url = get_url(lang,acc,spk)
    download_audio(url)
