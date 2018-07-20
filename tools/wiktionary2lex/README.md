# Wikitionary to Lexicon converter
Scripts for downloading, parsing and converting Wiktionary articles to lexicon
entries

## Third party resources
These scripts use a third party Python module to convert IPA in X-SAMPA.
The module can be downloaded [here](http://www.theiling.de/ipa/cxs.py), and the
required corresponding data table [here](http://www.theiling.de/ipa/CXS.def).
These should be stored in the third\_party/ directory.

## Parsers
There is a different parser for each language. Note that this is the language
the Wiktionary article is written in, not the language of the words themselves.
Any new parsers should be saved in the form parsers/[two-letter language code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).py
They must also be added to the import and the dictionary in get\_parser() in
parser\_lib.py
