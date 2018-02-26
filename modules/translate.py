#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 23:45:44 2018

@author: devnet
"""

from google.cloud import translate

class TranslateIntelligence():
    
    '''
    # Instantiate a translation client
    '''     
    def get_client(self):
        return translate.Client()
    
    def translate(self, client, data):
        return client.translate(data)
    
    def detect_language(self, client, data):
        return client.detect_language(data)
