#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 23:13:46 2018

@author: devnet
"""

import os
import six
import datetime

from ffmpy import FFmpeg
from google.cloud import storage
from config import Config
from werkzeug import secure_filename

config = Config()

class Common():
    
    '''
    # Convert an audio or video file into FLAC and set limit channels to 1
    '''
    def convert_to_flac(self, old, new):
        ff = FFmpeg(
                inputs={old: None},
                outputs={new: '-y -ac 1'})
        ff.run()
    
    '''
    # Convert an video file to flac
    '''  
    def convert_to_audio(self, old, new):
        ff = FFmpeg(
                inputs={old: None},
                outputs={new: '-y -acodec flac -ac 1 -bits_per_raw_sample 16 -ar 44100'})
        ff.run()
     
    '''
    # Convert video file to mp4 video
    '''
    def convert_to_mp4(self, old, new):
       ff = FFmpeg(
               inputs={old: None},
               outputs={new: '-y'})
       ff.run()  
       
    '''
    # Generic header for each available function
    ''' 
    def opening_label(self, labl):
        print('\n++++++++++++++++++++++++++++++++++++++++++')
        print(labl)
        print('++++++++++++++++++++++++++++++++++++++++++\n')
        
    '''
    # Instantiate a storage client
    '''     
    def get_storage_client(self):
        return storage.Client(project = config.PROJECT_ID)
    
    '''
    # Check if the file extention is allowed to be uploaded. 
    '''
    def check_extension(self, filename, allowed_extensions):
        if ('.' not in filename or filename.split('.').pop().lower() not in allowed_extensions):
            print("[!] {0} has an invalid name or extension".format(filename))
            return False
        else:
            return True
    
    def check_file_exists(self, filename):
        if not os.path.isfile(filename):
            print('[!] {0} is not a valid file on disk'.format(filename))
            return False
        else:
            return True
    
    '''
    # Generate a safe file name for upload. Name is generated based on the path
    # and datetime stamp
    '''
    def safe_filename(self, filename):
        """
        Generates a safe filename that is unlikely to collide with existing objects
        in Google Cloud Storage.
    
        ``filename.ext`` is transformed into ``filename-YYYY-MM-DD-HHMMSS.ext``
        """
        filename = secure_filename(filename)
        date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
        basename, extension = filename.rsplit('.', 1)
        return "{0}-{1}.{2}".format(basename, date, extension)
    
    '''
    # Upload the file to the designated bucket and receive the URL of the file
    '''
    def upload_file(self, file_stream, filename, content_type, bucket):
        """
        Uploads a file to a given Cloud Storage bucket and returns the public url
        to the new object.
        """
        file_exists = self.check_extension(filename, config.ALLOWED_EXTENSIONS)
        
        if not file_exists:
            return
        
        filename = self.safe_filename(filename)
    
        client = self.get_storage_client()
        bucket = client.bucket(bucket)
        blob = bucket.blob(filename)
    
        blob.upload_from_string(
            file_stream,
            content_type=content_type)
    
        url = blob.public_url
    
        if isinstance(url, six.binary_type):
            url = url.decode('utf-8')
    
        return url
