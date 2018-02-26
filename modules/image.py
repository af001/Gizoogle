#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 22:18:44 2018

@author: devnet
"""
import re

from google.cloud import vision
from common import Common
from config import Config

config = Config()
common = Common()
    
class ImageIntelligence():
    
    '''
    # Instantiate a image client
    '''     
    def get_client(self):
        return vision.ImageAnnotatorClient()
    
    '''
    # Run all ImageIntelligence functions
    '''
    def run_all(self, resp):
        self.print_face_details(resp)
        self.print_logo_details(resp)
        self.print_text_details(resp)
        self.print_label_details(resp)
        self.print_landmark_details(resp)
        self.print_web_details(resp)
        self.print_safe_search_details(resp)

    '''
    # Analyze an image and print the Google Image API response
    '''
    def analyze_image(self, URL, client):
        request = {'image': {'source': {'image_uri': URL},},}
        response = client.annotate_image(request)
        return response
    
    '''
    # Detect faces in an image and attempt to identify features that indicate
    # joy, sorrow, anger, surprise, and if the individual is wearing headgear
    '''    
    def print_face_details(self, response):
        common.opening_label('# FACE DETECTION')
        
        if len(response.face_annotations) > 0:
            print('[+] Detected %s face annotations...' % len(response.face_annotations))
    
            counter = 0
            for face in response.face_annotations:
                print('\n[+] Face %s detected with %s confidence...' % (counter+1, face.detection_confidence))
                print('\tJoy:\t\t%s' % config.CATEGORY[face.joy_likelihood])
                print('\tSorrow:\t\t%s' % config.CATEGORY[face.sorrow_likelihood])
                print('\tAnger:\t\t%s' % config.CATEGORY[face.anger_likelihood])
                print('\tSurprise:\t%s' % config.CATEGORY[face.surprise_likelihood])
                print('\tHeadwear:\t%s' % config.CATEGORY[face.headwear_likelihood])
                counter+=1
        else:
            print('[!] No faces found...')
    
    '''
    # Identify any logos that are in an image
    '''
    def print_logo_details(self, response):
        common.opening_label('# LOGO DETECTION')
    
        if len(response.logo_annotations) > 0:
            print('[+] Detected %s logo annotations...' % len(response.logo_annotations))
            
            counter = 0
            for logo in response.logo_annotations:
                print('\n[+] Logo %s detected with %s confidence...' % (counter+1, logo.score))
                print('\tDescription:\t%s' % logo.description)
                counter+=1
        if len(response.logo_annotations) == 0:
            print('[!] No logos found...')
    
    '''
    # Extract text annotations from a supplied image
    '''
    def print_text_details(self, response):
        common.opening_label('# TEXT DETECTION')
    
        output = []
        seen = set()
    
        if len(response.text_annotations) > 0:
            print('[+] Detected %s text annotations...' % len(response.text_annotations))
            print('\n[+] Extracted, unique text:')
            for text in response.text_annotations:
                text = text.description.strip()
                text = text.lower()
                text = re.sub('[^A-Za-z0-9]+', ' ', text)
                words = text.split()
                
                for word in words:
                    if word not in seen:
                        seen.add(word)
                        output.append(word)
                
                for word in output:
                    print(word + ' ')
        else:
            print('[!] No text found...')
    
    '''
    # Extract labels from a supplied image
    '''
    def print_label_details(self, response):
        common.opening_label('# LABEL DETECTION')
    
        output = []
        seen = set()
        if len(response.label_annotations) > 0:
            print('[+] Detected %s label annotations...' % len(response.label_annotations))
            print('\n[+] Extracted, unique labels:')
            for label in response.label_annotations:
                label = label.description
                if label not in seen:
                    seen.add(label)
                    output.append(label)
            for label in output:
                print(label + ' ')
        else:
            print('[!] No labels found...')
    
    '''
    # Identify landmarks observed in an image. If a landmark is observed and 
    # identified by Google, provide the coordinates. NOTE: In some testing on 
    # different platforms, this may return an error.
    '''
    def print_landmark_details(self, response):
        common.opening_label('# LANDMARK DETECTION')
    
        if len(response.landmark_annotations) > 0:
            print('[+] Detected %s landmark annotations...' % len(response.landmark_annotations))
    
            counter = 0
            for landmark in response.landmark_annotations:
                print('\n[+] Landmark %s detected with %s confidence...' % (counter+1, landmark.score))
                print('\tDescription:\t%s' % landmark.description)
                
                try:
                    lat = response.landmark_annotations._values[0].locations[0].lat_lng.latitude
                    lon = response.landmark_annotations._values[0].locations[0].lat_lng.longitude
                    print('\tCoordinates:\t%s,%s' % (lat, lon))
                except AttributeError:
                    # Works on OSX, but not my Linux computer ???
                    print('\tCoordinates:\tParse Error!')
                counter+=1
        else:
            print('[!] No landmarks found...')
    
    '''
    # Compare the image to other indexed images on Google; provide alternative 
    # locations of the file on the Internet, gain context to the what the image
    # is about, and find similar pages with similar content
    '''
    def print_web_details(self, response):
        common.opening_label('# WEB DETECTION')
            
        if len(response.web_detection.web_entities) > 0:
            print('[+] {} Unique web identifiers describe this image as:'.format(len(response.web_detection.web_entities)))
            print('{0:35} {1}'.format('DESCRIPTION','SCORE'))
        
            counter = 0
            for web in response.web_detection.web_entities:
                print('{0:35} {1}'.format(web.description, web.score))
                counter+=1
        else:
            print('[!] No web entities found...')
    
        if len(response.web_detection.full_matching_images) > 0:
            print('\n[+] {} sites are hosting this exact images:'.format(len(response.web_detection.full_matching_images)))
    
            for web in response.web_detection.full_matching_images:
                print('Url  :  {}'.format(web.url)) 
        else:
            print('[!] No full matching images found...')
      
        if len(response.web_detection.pages_with_matching_images) > 0:
            print('\n[+] {} sites host content with similar images:'.format(len(response.web_detection.pages_with_matching_images)))
    
            for web in response.web_detection.pages_with_matching_images:
                print('Url  :  {}'.format(web.url))         
        else:
            print('[!] No pages with matching images found...')
    
    '''
    # Identify if the supplied image contains adult, spoof, medical, violent,
    # or racy information / images
    '''
    def print_safe_search_details(self, response):
        common.opening_label('# SAFE SEARCH DETECTION')
    
        if response.safe_search_annotation is not None:
            print('[+] Image content summary:')
            print('\tAdult:\t\t%s' % config.CATEGORY[response.safe_search_annotation.adult])
            print('\tSpoof:\t\t%s' % config.CATEGORY[response.safe_search_annotation.spoof])
            print('\tMedical:\t%s' % config.CATEGORY[response.safe_search_annotation.medical])
            print('\tViolence:\t%s' % config.CATEGORY[response.safe_search_annotation.violence])
            print('\tRacy:\t\t%s' % config.CATEGORY[response.safe_search_annotation.racy])
        else:
            print('[!] No safe search attributes found...') 
