#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 22:54:11 2018

@author: devnet
"""

from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import speech
from translate import TranslateIntelligence

ti = TranslateIntelligence()

class AudioIntelligence():
    
    '''
    # Instantiate a audio client
    '''     
    def get_client(self):
        return speech.SpeechClient()
    
    '''
    # Analyze a long audio file and print the Google Speech API response
    '''
    def try_long_run(self, URL, client, code):
        # Auto-determine the language, translate, and transcribe in english.
        # Notify the user if a translation occured, the language detected,
        # and the confidence level that the audio is that language.
        #try:
        audio = types.RecognitionAudio(uri=URL)
        
        config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
                profanity_filter=False,
                sample_rate_hertz=44100,
                language_code=code)
            
        operation = client.long_running_recognize(config, audio)
        resp = operation.result()
        #except:
        #    print('[!] Error processing file. Check the file path!')
        #    return
        
        if resp is not None:
            client = ti.get_client()           
            lang = ti.detect_language(client, resp.results[0].alternatives[0].transcript)
     
            if lang['language'] is not 'en':
                print('[!] Audio is translated!!')
                print('Language   : {}\nConfidence : {}%'.format(lang['language'], round(lang['confidence']*100),2))
    
                translated = []
                for x in range(len(resp.results)):
                    lang = ti.translate(client, resp.results[x].alternatives[0].transcript)
                    translated.append(lang['translatedText'])
    
                print('\n[+] Transcript: {}'.format(' '.join(translated)))
            else:
                print('\n[+] Transcript: {}'.format(resp.results[0].alternatives[0].transcript))
        else:
            print('\n[!] Error processing audio file...\n')
    
    
    '''
    # Analyze a converted FLAC file and return the Google Speech API response
    '''
    def analyze_audio(self, URL, client, code):
        # Auto-determine the language, translate, and transcribe in english.
        # Notify the user if a translation occured, the language detected,
        # and the confidence level that the audio is that language.
        #try:
        audio = types.RecognitionAudio(uri=URL)
        
        config = types.RecognitionConfig(
                encoding='FLAC',
                profanity_filter=False,
                sample_rate_hertz=44100,
                language_code=code)
        
        resp = client.recognize(config, audio)
        #except:
        #    print('[!] Error processing file. Check the file path!')
        #    return
        
        if resp is not None:
            client = ti.get_client()           
            lang = ti.detect_language(client, resp.results[0].alternatives[0].transcript)
     
            if lang['language'] is not 'en':
                print('[!] Audio is translated!!')
                print('Language   : {}\nConfidence : {}%'.format(lang['language'], round(lang['confidence']*100),2))
    
                translated = []
                for x in range(len(resp.results)):
                    lang = ti.translate(client, resp.results[x].alternatives[0].transcript)
                    translated.append(lang['translatedText'])
    
                print('\n[+] Transcript: {}'.format(' '.join(translated)))
            else:
                print('\n[+] Transcript: {}'.format(resp.results[0].alternatives[0].transcript))
        else:
            print('\n[!] Error processing audio file...\n')
