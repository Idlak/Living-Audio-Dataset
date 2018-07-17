#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from third_party import cxs

def ipa2xsampa(ipa_text):
    F = file('third_party/CXS.def')
    cxs_table = cxs.make_table(F)
    utf8_ipa_text = unicode(ipatext, 'utf8')
    xsampa_text = cxs.ucipa2cxs(utf8_ipatext,cxs_table)
    return xsampa_text
