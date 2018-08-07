# Idlak Resources
Audio and text resources that can be used within IDLAK

Languages are required to be 2 letters, normally their 2 letter ISO code, see: [wiki article on ISO_639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

Accents are required to also be 2 letters.

Speakers are 3 letter codes. If a speaker was recorded in multiple languages this should be noted in the noted in the speaker's README and where possible their speaker code should be the same in both languages. It is highly recommended that the recording environment is noted in the README, including microphone, location, and the original sample rate. The audio should be saved in uncompressed .wav files and then zipped.

## Directory structure
Maintaining the directory structure is very important for the tools in IDLAK.

### Language resources

* __ln__
  * text 
    * *source.xml*
  * `README.md`
  * word_frequencies.xml
  * *other resources in xml*

"word_frequencies.xml" is an example not a requirement.

See below for the text source format. Source names should be a reasonable name. If a source is really only for one region or accent it is recommended that the source file name starts with region and an underscore, for example: "uk_bbc.xml". For this reason we recommend not including underscores in your file names. We also recommend not to include spaces in file names.

### Text source format

We recommend keeping files to a reasonable size (under 5000 lines)

The text source xml format is:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<text_sources>
  <text_source id="unique within file" name="any name" url="original url">
    <notes>
      Notes here are ignored and this section is optional.
      other than id all attributes are optional in the text_source tag 
    </notes>
    <text>
      Text source here, utf8-encoded.
    </text>
  </text_source>
  <text_source />
  <text_source />
  <text_source />
</text_sources>
```

### Speaker resources

* __ln_ac_spk__
  * `README.md`
  * `script.xml`
  * `lexicon.xml`

Audio is uploaded to archive.org in tar.gz format

The script can note the pronunciation of specific words by the speaker with `<pron>` tags.

The lexicon is optional and will be appended to the language lexicon in the IDLAK main repo.

## Current speakers

| Language | Accent | Code | Notes |
|:--------:|:------:|:----:| ----- |
| en | rp | aaa | __example to be deleted__ |
