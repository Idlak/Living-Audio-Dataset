# Parses the xml of all English language Wiktionary articles (found here: https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles.xml.bz2 )
# Extracts all words from the specified language and their pronunciations
# Usage is python en_wiktionary_parser.py [Wiktionary xml file] [Language to extract]
# Language name is case sensitive and much match what Wiktionary uses
# Words and their pronunciations are output to pronunciations_[language]_[timestamp].txt
# Actions performed on all entries are logged in log_[language]_[timestamp].txt
from lxml import etree as ET
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv) != 3:
    print "Usage is python " + sys.argv[0] + " [Wiktionary xml file] [Language to extract]"
    exit(1)

print "Starting parse"
tree = ET.parse(sys.argv[1])
print "Finished parse"
root = tree.getroot()

language = sys.argv[2]

# Create output files
# Add timestamp to avoid overwriting results from other runs
timestr = time.strftime("%Y%m%d-%H%M%S")
pronunciations_filename = "pronunciations_" + language + "_" + timestr + ".txt"
log_filename = "log_" + language + "_" + timestr + ".txt"
pronunciations = open(pronunciations_filename,'w')
log = open(log_filename,'w')

# Language headings on Wiktionary are in the form ==[Language]==
language_section = "==" + language + "=="

for index, entry in enumerate(root):
	if index % 100000 == 0:
		print "Entry " + str(index)
	log.write(str(index) + " " + entry[0].text + "\n")

	# The field containing the actual text for the article is always in entry[3]
	for subentry in entry[3]:

		# Matches the subentry containing the data we need
		if subentry.tag == '{http://www.mediawiki.org/xml/export-0.10/}text':

			# Some entries have empty text fields that break the parser otherwise
			if subentry.text is None:
				break

			# Check that the article contains an entry for the relevant language
			if language_section in subentry.text:

				# Discard everything up to the name of the relevant language
				discard, keep = subentry.text.split(language_section,1)

				# ---- is the the marker for boundaries between languages
				# Discard everthing after it if it exists
				if "----" in keep:
					keep, discard = keep.split("----",1)

				# Discard everything up to the pronunciation section	
				if "===Pronunciation===" in keep:
					discard, keep = keep.split("===Pronunciation===",1)
				else:
					log.write("\t" + entry[0].text + " has no " + language + " pronunciation data\n")
					break

				# Discard everything after the pronunciation section
				# (The next section will always start with = if it exists)
				if "\n=" in keep:
					keep, discard = keep.split("\n=",1)

				# Discard first line for aesthetic purposes
				discard, keep = keep.split("\n",1)

				# Write word and pronunciation to file
				pronunciations.write(entry[0].text + "\n" + keep + "\n----\n\n")
				log.write("\t" + entry[0].text + " pronunciation written to file\n")
			else:
				log.write("\t" + entry[0].text + " is not a word in " + language + "\n")
