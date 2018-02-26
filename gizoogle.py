#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Giz00gle - Google API Testing and Evaluation. The primary libraries
# that are tested incldue the Google Speech API, VideoIntelligence API
# Translation API, and Image API
#
#
# CAO: 1826 February 4th, 2017
#
#################################################################

from __future__ import print_function
from __future__ import absolute_import

import re
import os

from cmd import Cmd
from pyfiglet import Figlet
from werkzeug.datastructures import FileStorage

from modules.image import ImageIntelligence
from modules.video import VideoIntelligence
from modules.audio import AudioIntelligence
from modules.translate import TranslateIntelligence
from modules.config import Config
from modules.common import Common

# Main prompt for the application. Used instead of a while loop. Uses keywords
# to trigger functions.
class GooglePrompt(Cmd):
    
    '''
    # Initial logo and version display
    '''
    def preloop(self):
        fig = Figlet(font='big')
        print(fig.renderText('GizOOgle'))
        print('Version 1.0a')
    
    '''
    # Analyze an image from the Internet or from a local file
    Usage:
        image <gs://<bucket>/file.jpeg     : Analyze an image in your bucket
        image https://myfile.com/file.jpeg : Analyze an image on a webpage
        image /home/devnet/file.jpeg       : Convert, upload, and analyze
    '''
    def do_image(self, path):        
        common.opening_label('# IMAGE ANALYSIS')

        # Instantiate a image client
        ii = ImageIntelligence()
        client = ii.get_client()
        resp = None
        
        # Get file by URI, else upload local file
        if path.startswith('http') or path.startswith('gs:'):
            resp = ii.analyze_image(path, client)
        else:
            file_exists = common.check_file_exists(path)           
            if not file_exists:
                return
            
            with open(path, 'rb') as fp:
                img = FileStorage(fp)
                url = common.upload_file(img.read(), img.filename, img.content_type, 
                                  config.IMAGE_STORAGE_BUCKET)
                if url is not '':
                    resp = ii.analyze_image(url, client)
                else:
                    return
                
        # Run all ImageIntelligence modules and print results
        if resp is not None:
            ii.run_all(resp)
    
    '''
    # Display information about the do_audio command
    Usage:
        help image
    '''
    def help_image(self):
        print('image <url>\nimage <local_path>\nImage analysis using Google Vision')
    
    '''
    # Transcribe an audio file and attempt to auto-translate to english
    Usage:
        audio <lang> <gs://<bucket>/file.flac : Analyze a FLAC file in your bucket
        audio <lang> /home/devnet/file.mp3    : Convert, upload, and analyze
    '''
    def do_audio(self, arg):    
        common.opening_label('# AUDIO TRANSCRIPTION')
 
        # Split the arg variable        
        x = arg.split(' ')       
        code = x[0]
        path = x[1]
                      
        # Instantiate a speech client
        ai = AudioIntelligence()
        client = ai.get_client()
        
        # Determine if the file is remote or local. If the file is large,
        # then use try_long_run. File must be flac if remote, and in the 
        # bucket gs://bucket_name/file.flac
        if path.startswith('gs:') and path.endswith('flac'):
            try:
                ai.analyze_audio(path, client, code)
            except:
                ai.try_long_run(path, client, code)
        else:
            fileExists = common.check_file_exists(path)
            if not fileExists:
                return 
            
            # Convert the audio to FLAC and upload to audio bucket. Assuming
            # the file is not FLAC here. Save the file in the same path.
            base = os.path.splitext(path)[0]
            new_path = base + '.flac'
            common.convert_to_flac(path, new_path)
            
            # Open and upload the file to the storage bucket. Split resulting
            # URL to get the filename and use the same gs:// method to analyze
            # the FLAC audio file.
            with open(new_path, 'rb') as fp:
                audio = FileStorage(fp)
                url = common.upload_file(audio.read(), audio.filename, audio.content_type, config.AUDIO_STORAGE_BUCKET)
                if url is not '':
                    gs_file = url.split("/")[-1]
                    try:
                        ai.analyze_audio('gs://' + Config.AUDIO_STORAGE_BUCKET + '/' + gs_file, client, code)
                    except:
                        ai.try_long_run('gs://' + Config.AUDIO_STORAGE_BUCKET + '/' + gs_file, client, code)
                else:
                    return
        
    '''
    # Display information about the do_audio command
    Usage:
        help audio
    '''
    def help_audio(self):
        print('audio <lang_code> <gs://<bucket_name>/<file_name>>\naudio <lang_code> <local_path>\nSpeech analysis using Google Speech')
    
        '''
    # Analyze a video file and attempt to auto-translate and transcribe to english
    Usage:
        video <lang> <gs://<bucket>/file.mp4  : Analyze a FLAC file in your bucket
        video <lang> /home/devnet/file.avi    : Convert, upload, and analyze
    '''
    def do_video(self, arg):
        common.opening_label('# VIDEO ANALYSIS')
                      
        # Split the arg variable
        x = arg.split(' ')      
        code = x[0]
        path = x[1]
        
        # Instantiate a videointelligence client
        vi = VideoIntelligence()
        client = vi.get_client()
        
        # If the video is already uploaded, process the file. If the file is
        # local, upload the video and process. 
        if path.startswith('gs:'):
            vi.analyze_video(path, client)
        else:
            file_exists = common.check_file_exists(path)
            if not file_exists:
                return
            
            with open(path, 'rb') as fp:
                video = FileStorage(fp)
                url = common.upload_file(video.read(), video.filename, video.content_type, config.VIDEO_STORAGE_BUCKET)
                if url is not '':
                    gs_file = url.split("/")[-1]
                    vi.analyze_video('gs://' + config.VIDEO_STORAGE_BUCKET + '/' + gs_file, client)
                else:
                    return

            # Convert the video file to a mp4, then convert the video file
            # to FLAC. Unable to directly convert some formats to FLAC, so 
            # first convert to mp4, then FLAC.
            base = os.path.splitext(path)[0]
            
            # There is a bug with some video to audio conversions. This primarily
            # occurs when converting avi to mp4, then from mp4 to FLAC.
            # TODO: Fix alternative video formats to FLAC
            if path.endswith('.mp4') or path.endswith('.MP4'):
                new_path = path
            else:
                new_path = base + '.mp4'
                common.convert_to_mp4(path, new_path)

            # Convert the mp4 to FLAC
            new_path_audio = base + '.flac'
            common.convert_to_audio(new_path, new_path_audio)
            
            # Analyze the FLAC and transcribe.
            with open(new_path_audio, 'rb') as fp:
                audio = FileStorage(fp)
                url = common.upload_file(audio.read(), audio.filename, audio.content_type, config.AUDIO_STORAGE_BUCKET)
                if url is not '':
                    ai = AudioIntelligence()
                    client = ai.get_client()
                    gs_file = url.split("/")[-1]
                    try:
                        ai.analyze_audio('gs://' + config.AUDIO_STORAGE_BUCKET + '/' + gs_file, client, code)
                    except:
                        ai.try_long_run('gs://' + config.AUDIO_STORAGE_BUCKET + '/' + gs_file, client, code)
                else:
                    return
                    
    '''
    # Display information about the do_audio command
    Usage:
        help video
    '''
    def help_video(self):
        print('video <lang_code> <gs://<bucket_name>/<file_name>>\nvideo <lang_code> <local_path>\nAnalyze video with Google Intelligence API')

    '''
    # Translate a document locally or one on the Internet
    Usage:
        translate gs://<bucket>/file.txt        : Translate from a bucket
        translate https://myfile.com/index.html : Translate from a URL
        translate /home/devnet/file.txt         : Translate from local file
    '''    
    def do_translate(self, path):
        common.opening_label('# DOCUMENT TRANSLATION')
        
        # Instantiate a translate client
        ti = TranslateIntelligence()
        client = ti.get_client()
        
        # Determine if remote or local file.
        if path.startswith('http') or path.startswith('gs:'):
            pass # TODO: Fetch URL, parse w/ beautiful soup
        else:
            file_exists = common.check_file_exists(path)
            if not file_exists:
                return
            
            # Read document into memory
            with open(path) as f:
                data = f.readline()
            
            # First detect the language
            resp = ti.detect_language(client, data)
            print('Language: {}\nConfidence: {}%'.format(resp['language'], round(resp['confidence']*100),2))
        
            # Translate the document and display the output to the user            
            with open(path) as f:
                data = f.readlines()
                
            resp_trans = ti.translate(client, data)
            print('\nTranslation:')
            for text in resp_trans:
                print(text['translatedText'])

    '''
    # Display information about the do_audio command
    Usage:
        help translate
    '''    
    def help_translate(self):
        print('translate gs://<bucket>/file.txt')
        print('translate <text_file>\nTranslate a local or remote document')

    '''
    # Identify the appropriate language code for translation / speech recognition
    Usage:
        lang           : display a complete list of available languages
        lang arabic    : search for a language code associated with "arabic"
    '''
    def do_lang(self, search_term):
        # Allow user to search available language codes. Used for audio
        # and video analysis; specifically do_video and do_audio
        if search_term:
            re_search = re.compile(search_term, re.IGNORECASE)
            print('{0:12} {1}'.format('CODE', 'DESCRIPTION'))
            for key, value in config.LANGUAGE.iteritems():
                if re_search.search(value):
                    print('{0:12} {1}'.format(key, value))           
        else:
            # If no arg is given, show all available languages and their
            # respective descriptions
            print('\n{0:12} {1}'.format('CODE', 'DESCRIPTION'))
            for lang in config.LANGUAGE:
                print('{0:12} {1}'.format(lang, config.LANGUAGE[lang]))

    '''
    # Display information about the do_audio command
    Usage:
        help lang
    '''            
    def help_lang(self):
        print('lang\nlang <search-term>\nLocate a language code for translation or speech')
                

'''
############ START SCRIPT ###############
'''
common = Common()
config = Config()

def main():
    print()
    prompt = GooglePrompt()
    prompt.prompt = '> '
    prompt.cmdloop('\nThey\'ve done studies you know. Sixty percent of the time it works every time....')

if __name__ == '__main__':
    main()
