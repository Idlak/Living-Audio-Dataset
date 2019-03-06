# IPA to Phoneset converter
Scripts that add an Idlak phoneset pronunciation to a lexicon by converting from
IPA using greedy matching.

## ipa2lex.py
Takes a lexicon and an IPA-to-phone mapping, both in xml form.

Example lexicon:
```
<?xml version="1.0"?>
<lexicon name="cmudict.0.7a">
<lex ipa="ɛɪ" entry="full" default="true">a</lex>
<lex ipa="ˈtrɪpl ɛɪ" entry="full" default="true">aaa</lex>
<lex ipa="ˈbæblɪŋ" entry="full" default="true">babbling</lex>
<lex ipa="kriːm" entry="full" default="true">cream</lex>
<lex ipa="daɪˈnæmɪk" entry="full" default="true">dynamic</lex>
</lexicon>
```

Example mapping:
```
<?xml version='1.0' encoding='UTF-8'?>
<ipa_mapping>
  <map pron="ae" ipa="æ"/>
  <map pron="ay" ipa="aɪ"/>
  <map pron="b" ipa="b"/>
  <map pron="d" ipa="d"/>
  <map pron="ey" ipa="ɛɪ"/>
  <map pron="ih" ipa="ɪ"/>
  <map pron="iy" ipa="i"/>
  <map pron="k" ipa="k"/>
  <map pron="l" ipa="l"/>
  <map pron="m" ipa="m"/>
  <map pron="n" ipa="n"/>
  <map pron="ng" ipa="ŋ"/>
  <map pron="p" ipa="p"/>
  <map pron="r" ipa="r"/>
  <map pron="t" ipa="t"/>
</ipa_mapping>
```

Outputs another lexicon with the pronunciation added, as well an an attribute
noting the origin of the pronunciation.

Example output:
```
<?xml version='1.0' encoding='UTF-8'?>
<lexicon name="cmudict.0.7a">
<lex ipa="ɛɪ" entry="full" default="true" pron="ey" provenance="IPA conversion">a</lex>
<lex ipa="ˈtrɪpl ɛɪ" entry="full" default="true" pron="t r ih p l ey" provenance="IPA conversion">aaa</lex>
<lex ipa="ˈbæblɪŋ" entry="full" default="true" pron="b ae b l ih ng" provenance="IPA conversion">babbling</lex>
<lex ipa="kriːm" entry="full" default="true" pron="k r iy m" provenance="IPA conversion">cream</lex>
<lex ipa="daɪˈnæmɪk" entry="full" default="true" pron="d ay n ae m ih k" provenance="IPA conversion">dynamic</lex>
</lexicon>
```

Any unrecognised characters will be skipped over with a warning.

## phoneset2ipamap.py
Takes a phoneset xml as input and outputs a mapping xml that can be used by
ipa2lex.py.

Example input:
```
<?xml version="1.0" encoding="UTF-8"?>
<phonesetup>
	<phone name="ae">
		<description word_example="trap" pron_example="t_r_ae_p" ipa="æ" archiphone="false"/>
	</phone>
	<phone name="ay">
		<description word_example="rice" pron_example="r_ay_s" ipa="aɪ" archiphone="false"/>
	</phone>
	<phone name="b">
		<description word_example="bee" pron_example="b_iy" ipa="b" archiphone="false"/>
	</phone>
	<phone name="d">
		<description word_example="dye" pron_example="d_ai" ipa="d" archiphone="false"/>
	</phone>
	<phone name="ey">
		<description word_example="face" pron_example="f_ey_s" ipa="ɛɪ" archiphone="false"/>
	</phone>
	<phone name="ih">
		<description word_example="hit" pron_example="h_ih_t" ipa="ɪ" archiphone="false"/>
	</phone>
	<phone name="iy">
		<description word_example="fleece" pron_example="f_l_iy_s" ipa="i" archiphone="false"/>
	</phone>
	<phone name="k">
		<description word_example="key" pron_example="k_iy" ipa="k" archiphone="false"/>
	</phone>
	<phone name="l">
		<description word_example="lay" pron_example="l_ey" ipa="l" archiphone="false"/>
	</phone>
	<phone name="m">
		<description word_example="me" pron_example="m_iy" ipa="m" archiphone="false"/>
	</phone>
	<phone name="n">
		<description word_example="knee" pron_example="n_iy" ipa="n" archiphone="false"/>
	</phone>
	<phone name="ng">
		<description word_example="song" pron_example="s_o_ng" ipa="ŋ" archiphone="false"/>
	</phone>
	<phone name="p">
		<description word_example="pea" pron_example="p_iy" ipa="p" archiphone="false"/>
	</phone>
	<phone name="r">
		<description word_example="ray" pron_example="r_ey" ipa="r" archiphone="false"/>
	</phone>
	<phone name="t">
		<description word_example="tea" pron_example="t_iy" ipa="t" archiphone="false"/>
	</phone>
</phonesetup>
```

Example output:
```
<?xml version='1.0' encoding='UTF-8'?>
<ipa_mapping>
  <map pron="ae" ipa="æ"/>
  <map pron="ay" ipa="aɪ"/>
  <map pron="b" ipa="b"/>
  <map pron="d" ipa="d"/>
  <map pron="ey" ipa="ɛɪ"/>
  <map pron="ih" ipa="ɪ"/>
  <map pron="iy" ipa="i"/>
  <map pron="k" ipa="k"/>
  <map pron="l" ipa="l"/>
  <map pron="m" ipa="m"/>
  <map pron="n" ipa="n"/>
  <map pron="ng" ipa="ŋ"/>
  <map pron="p" ipa="p"/>
  <map pron="r" ipa="r"/>
  <map pron="t" ipa="t"/>
</ipa_mapping>
```
