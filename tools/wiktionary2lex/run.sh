#!/bin/bash

output="lex.xml"

if [ $# -eq 0 ]
    then
        language_code="en"
    else
        language_code=$1
fi

FILE=$language_code"wiktionary-latest-pages-articles-multistream.xml"
DIRECTORY="wiktionaries/"
DFILE=$DIRECTORY$FILE

if [ ! -f third_party/cxs.py ]
    then
        wget http://www.theiling.de/ipa/cxs.py
        mv cxs.py third_party
fi

if [ ! -f third_party/CXS.def ]
    then
        wget http://www.theiling.de/ipa/CXS.def
        mv CXS.def third_party
fi

if [ ! -f $DFILE ]
    then
        ZIPFILE=$FILE".bz2"
        DZIPFILE=$DIRECTORY$ZIPFILE

        if [ ! -f $DZIPFILE ]
            then
                wget "https://dumps.wikimedia.org/gawiktionary/latest/"$ZIPFILE
                mkdir -p $DIRECTORY
                mv $ZIPFILE $DZIPFILE
        fi
        bzip2 -dk $DZIPFILE
fi

./wiktionary2lex.py $language_code $DFILE $output
