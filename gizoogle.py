#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# To authenticate, download your json keyfile from your account.
# Once done, run the following command in a terminal, or set the
# export in your ~/.bashrc or ~/.profile
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/keyfile.json"
#
#
# CAO: 1826 February 4th, 2017
#
#################################################################

from __future__ import print_function
from __future__ import absolute_import

import re
import os
import six
import datetime
import ffmpeg

from cmd import Cmd
from pyfiglet import Figlet
from google.cloud.vision_v1 import ImageAnnotatorClient
from google.cloud import videointelligence
from google.cloud import storage
from google.cloud import speech
from google.cloud import translate
from google.cloud.speech import enums
from google.cloud.speech import types
from werkzeug import secure_filename
from werkzeug.exceptions import BadRequest
from werkzeug.datastructures import FileStorage

# Main prompt for the application. Used instead of a while loop. Uses keywords
# to trigger functions.
class GooglePrompt(Cmd):
    
    '''
    # This is the "do" section. Define a function with do_xyz and you can use
    # xyz <arg> to call the function from the custom cmd prompt. There are
    # alternative, predefined functions you can override.
    # References:
    1. https://pymotw.com/2/cmd/
    2. https://coderwall.com/p/w78iva/give-your-python-program-a-shell-with-the-cmd-module
    '''
    
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
        
        # Instantiate a speech client
        client = ImageAnnotatorClient()
        resp = None
        
        # Get file by URI, else upload local file
        if path.startswith('http') or path.startswith('gs:'):
            resp = analyze_image(path, client)
        else:
            # TODO: Check if the file exists
            with open(path, 'rb') as fp:
                img = FileStorage(fp)
                url = upload_file(img.read(), img.filename, img.content_type, IMAGE_STORAGE_BUCKET)
                if url is not '':
                    resp = analyze_image(url, client)
                
        # Process and extract as much data as possible. We upload to limit the
        # number of API calls. 
        if resp is not None:
            print_face_details(resp)
            print_logo_details(resp)
            print_text_details(resp)
            print_label_details(resp)
            print_landmark_details(resp)
            print_web_details(resp)
            print_safe_search_details(resp)
        else:
            print('[!] Error processing image...')
    
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
        audio <gs://<bucket>/file.flac : Analyze a FLAC file in your bucket
        audio /home/devnet/file.mp3    : Convert, upload, and analyze
    '''
    def do_audio(self, path):    
        opening_label('# AUDIO TRANSCRIPTION')
        
        # Instantiate a speech client
        client = speech.SpeechClient()
        resp = None
        
        # Determine if the file is remote or local. If the file is large,
        # then use try_long_run. File must be flac if remote, and in the 
        # bucket gs://bucket_name/file.flac
        if path.startswith('gs:') and path.endswith('flac'):
            try:
                resp = analyze_audio(path, client)
            except:
                resp = try_long_run(path, client)
        else:
            # Convert the audio to FLAC and upload to audio bucket. Assuming
            # the file is not FLAC here. Save the file in the same path.
            base = os.path.splitext(path)[0]
            new_path = base + '.flac'
            convert_to_flac(path, new_path)
            
            # Open and upload the file to the storage bucket. Split resulting
            # URL to get the filename and use the same gs:// method to analyze
            # the FLAC audio file.
            with open(new_path, 'rb') as fp:
                audio = FileStorage(fp)
                url = upload_file(audio.read(), audio.filename, audio.content_type, AUDIO_STORAGE_BUCKET)
                if url is not '':
                    gs_file = url.split("/")[-1]
                    try:
                        resp = analyze_audio('gs://'+AUDIO_STORAGE_BUCKET+'/'+gs_file, client)
                    except:
                        resp = try_long_run('gs://'+AUDIO_STORAGE_BUCKET+'/'+gs_file, client)
        
        # Auto-determine the language, translate, and transcribe in english.
        # Notify the user if a translation occured, the language detected,
        # and the confidence level that the audio is that language.
        if resp is not None:
            client = translate.Client()           
            lang = client.detect_language(resp.results[0].alternatives[0].transcript)
 
            if lang['language'] is not 'en':
                print('[!] Audio is translated!!')
                print('Language   : {}\nConfidence : {}%'.format(lang['language'], round(lang['confidence']*100),2))
                
                translated = []
                for x in range(len(resp.results)):
                    lang = client.translate(resp.results[x].alternatives[0].transcript)
                    translated.append(lang['translatedText'])

                print('\n[+] Transcript: {}'.format(' '.join(translated)))
            else:
                print('\n[+] Transcript: {}'.format(resp.results[0].alternatives[0].transcript))
            
            
        else:
            print('\n[!] Error processing audio file...\n')
    
    '''
    # Display information about the do_audio command
    Usage:
        help audio
    '''
    def help_audio(self):
        print('audio <gs://<bucket_name>\naudio <local_path>\nSpeech analysis using Google Speech')
    
    
    def do_video(self, path):
        if path.startswith('http') or path.startswith('gs:'):
            pass # TODO: Fetch URL, convert to mp3 if video, translate
        else:
            pass # TODO: Read file, convert to mp3 if video, translate

    '''
    # Translate a document locally or one on the Internet
    Usage:
        translate gs://<bucket>/file.txt        : Translate from a bucket
        translate https://myfile.com/index.html : Translate from a URL
        translate /home/devnet/file.txt         : Translate from local file
    '''    
    def do_translate(self, path):
        opening_label('# DOCUMENT TRANSLATION')
        
        # Instantiate a translate client
        client = translate.Client() 
        
        # Determine if remote or local file.
        if path.startswith('http') or path.startswith('gs:'):
            pass # TODO: Fetch URL, parse w/ beautiful soup
        else:
            # Read document into memory
            with open(path) as f:
                data = f.readline()
            
            # First detect the language
            resp = client.detect_language(data)
            print('Language: {}\nConfidence: {}%'.format(resp['language'], round(resp['confidence']*100),2))
        
            # Translate the document and display the output to the user            
            resp = client.translate(data)
            print('\nTranslation:')
            for text in resp:
                print(text['translatedText'])
            
            # TODO: Store to txt and upload to server
            #with open(path, 'rb') as fp:
            #    document = FileStorage(fp)
            #    url = upload_file(document.read(), document.filename, document.content_type, DOCUMENT_STORAGE_BUCKET)

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
            for key, value in LANGUAGE.iteritems():
                if re_search.search(value):
                    print('{0:12} {1}'.format(key, value))           
        else:
            # If no arg is given, show all available languages and their
            # respective descriptions
            print('\n{0:12} {1}'.format('CODE', 'DESCRIPTION'))
            for lang in LANGUAGE:
                print('{0:12} {1}'.format(lang, LANGUAGE[lang]))

    '''
    # Display information about the do_audio command
    Usage:
        help lang
    '''            
    def help_lang(self):
        print('lang\nlang <search-term>\nLocate a language code for translation or speech')

'''
# Convert an audio or video file into FLAC and set limit channels to 1
# Overwrite any existing file that exists locally with the new one
'''
def convert_to_flac(old, new):
    stream = ffmpeg.input(old)
    stream = ffmpeg.output(stream, new, ac=1).overwrite_output()
    ffmpeg.run(stream)

'''
# Check if a referenced local file exists before performing operations
'''
def check_file_exists(path):
    pass # Check file exists, return true / false

'''
# Generic header for each available function
''' 
def opening_label(labl):
    print('\n++++++++++++++++++++++++++++++++++++++++++')
    print(labl)
    print('++++++++++++++++++++++++++++++++++++++++++\n')

'''
# Analyze an image and return the Google Image API response
'''
def analyze_image(URL, client):
    request = {'image': {'source': {'image_uri': URL},},}
    response = client.annotate_image(request)
    return response

'''
# Analyze a long audio file and return the Google Speech API response
'''
def try_long_run(URL, client):
    audio = types.RecognitionAudio(uri=URL)

    config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
            profanity_filter=False,
            sample_rate_hertz=44100,
            language_code='ru-RU')
    
    operation = client.long_running_recognize(config, audio)
    
    return operation.result()

'''
# Analyze a converted FLAC file and return the Google Speech API response
'''
def analyze_audio(URL, client):
    audio = types.RecognitionAudio(uri=URL)

    config = types.RecognitionConfig(
            encoding='FLAC',
            profanity_filter=False,
            sample_rate_hertz=44100,
            language_code='ru-RU')

    response = client.recognize(config, audio)
    return response

'''
# Detect faces in an image and attempt to identify features that indicate
# joy, sorrow, anger, surprise, and if the individual is wearing headgear
'''    
def print_face_details(response):
    opening_label('# FACE DETECTION')
    
    if len(response.face_annotations) > 0:
        print('[+] Detected %s face annotations...' % len(response.face_annotations))

        counter = 0
        for face in response.face_annotations:
            print('\n[+] Face %s detected with %s confidence...' % (counter+1, face.detection_confidence))
            print('\tJoy:\t\t%s' % category[face.joy_likelihood])
            print('\tSorrow:\t\t%s' % category[face.sorrow_likelihood])
            print('\tAnger:\t\t%s' % category[face.anger_likelihood])
            print('\tSurprise:\t%s' % category[face.surprise_likelihood])
            print('\tHeadwear:\t%s' % category[face.headwear_likelihood])
            counter+=1
    else:
        print('[!] No faces found...')

'''
# Identify any logos that are in an image
'''
def print_logo_details(response):
    opening_label('# LOGO DETECTION')

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
def print_text_details(response):
    opening_label('# TEXT DETECTION')

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
                print(word, end=" ")
            print('')
    else:
        print('[!] No text found...')

'''
# Extract labels from a supplied image
'''
def print_label_details(response):
    opening_label('# LABEL DETECTION')

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
            print(label, end=" ")
            print('')
    else:
        print('[!] No labels found...')

'''
# Identify landmarks observed in an image. If a landmark is observed and 
# identified by Google, provide the coordinates. NOTE: In some testing on 
# different platforms, this may return an error.
'''
def print_landmark_details(response):
    opening_label('# LANDMARK DETECTION')

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
def print_web_details(response):
    opening_label('# WEB DETECTION')
        
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
def print_safe_search_details(response):
    opening_label('# SAFE SEARCH DETECTION')

    if response.safe_search_annotation is not None:
        print('[+] Image content summary:')
        print('\tAdult:\t\t%s' % category[response.safe_search_annotation.adult])
        print('\tSpoof:\t\t%s' % category[response.safe_search_annotation.spoof])
        print('\tMedical:\t%s' % category[response.safe_search_annotation.medical])
        print('\tViolence:\t%s' % category[response.safe_search_annotation.violence])
        print('\tRacy:\t\t%s' % category[response.safe_search_annotation.racy])
    else:
        print('[!] No safe search attributes found...') 

'''
# Instantiate a storage client
'''     
def _get_storage_client():
    return storage.Client(project=PROJECT_ID)

'''
# Check if the file extention is allowed to be uploaded. 
'''
def _check_extension(filename, allowed_extensions):
    if ('.' not in filename or filename.split('.').pop().lower() not in allowed_extensions):
        raise BadRequest("{0} has an invalid name or extension".format(filename))

'''
# Generate a safe file name for upload. Name is generated based on the path
# and datetime stamp
'''
def _safe_filename(filename):
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
def upload_file(file_stream, filename, content_type, bucket):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """
    _check_extension(filename, ALLOWED_EXTENSIONS)
    filename = _safe_filename(filename)

    client = _get_storage_client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(filename)

    blob.upload_from_string(
        file_stream,
        content_type=content_type)

    url = blob.public_url

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url

'''
############ START SCRIPT ###############
'''
# TODO: Clean up these variables with a config file
IMAGE_STORAGE_BUCKET = 'image_dump' # Change this to your image bucket
AUDIO_STORAGE_BUCKET = 'speech_dump' # Change this to your speech bucket
DOCUMENT_STORAGE_BUCKET = 'document_dump' # Change this to your document bucket
VIDEO_STORAGE_BUCKET = 'video_dump' # Change this to your video bucket
PROJECT_ID = 'analysis-283736' # Change this to your project-ID

MAX_CONTENT_LENGTH = 8 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'flac', 'txt'])
LANGUAGE = {
        "af-ZA": "Afrikaans (South Africa)", 
        "am-ET": "Amharic (Ethiopia)", 
        "hy-AM": "Armenian (Armenia)", 
        "az-AZ": "Azerbaijani (Azerbaijan)", 
        "id-ID": "Indonesian (Indonesia)", 
        "ms-MY": "Malay (Malaysia)", 
        "bn-BD": "Bengali (Bangladesh)", 
        "bn-IN": "Bengali (India)", 
        "ca-ES": "Catalan (Spain)", 
        "cs-CZ": "Czech (Czech)", 
        "da-DK": "Danish (Denmark)", 
        "de-DE": "German (Germany)", 
        "en-AU": "English (Australia)", 
        "en-CA": "English (Canada)", 
        "en-GH": "English (Ghana)", 
        "en-GB": "English (United Kingdon)", 
        "en-IN": "English (India)", 
        "en-IE": "English (Ireland)", 
        "en-KE": "English (Kenya)", 
        "en-NZ": "English (New Zealand)", 
        "en-NG": "English (Nigeria)", 
        "en-PH": "English (Philippines)", 
        "en-ZA": "English (South Africa)", 
        "en-TZ": "English (Tanzania)", 
        "en-US": "English (United States)", 
        "es-AR": "Spanish (Argentina)", 
        "es-BO": "Spanish (Bolivia)", 
        "es-CL": "Spanish (Chile)", 
        "es-CO": "Spanish (Colombia)", 
        "es-CR": "Spanish (Costa Rica)", 
        "es-EC": "Spanish (Ecuador)", 
        "es-SV": "Spanish (El Salvador)", 
        "es-ES": "Spanish (Spain)", 
        "es-US": "Spanish (United States)", 
        "es-GT": "Spanish (Guatemala)", 
        "es-HN": "Spanish (Honduras)", 
        "es-MX": "Spanish (Mexico)", 
        "es-NI": "Spanish (Nicaragua)", 
        "es-PA": "Spanish (Panama)", 
        "es-PY": "Spanish (Paraguay)", 
        "es-PE": "Spanish (Peru)", 
        "es-PR": "Spanish (Puerto)", 
        "es-DO": "Spanish (Dominican Republic)", 
        "es-UY": "Spanish (Uruguay)", 
        "es-VE": "Spanish (Venezuela)", 
        "eu-ES": "Basque (Spain)", 
        "fil-PH": "Filipino (Philippines)", 
        "fr-CA": "French (Canada)", 
        "fr-FR": "French (France)", 
        "gl-ES": "Galician (Spain)", 
        "ka-GE": "Georgian (Georgia)", 
        "gu-IN": "Gujarati (India)", 
        "hr-HR": "Croatian (Croatia)", 
        "zu-ZA": "Zulu (South Africa)", 
        "is-IS": "Icelandic (Iceland)", 
        "it-IT": "Italian (Italy)", 
        "jv-ID": "Javanese (Indonesia)", 
        "kn-IN": "Kannada (India)", 
        "km-KH": "Khmer (Cambodia)", 
        "lo-LA": "Lao (Laos)", 
        "lv-LV": "Latvian (Latvia)", 
        "lt-LT": "Lithuanian (Lithuania)", 
        "hu-HU": "Hungarian (Hungary)", 
        "ml-IN": "Malayalam (India)", 
        "mr-IN": "Marathi (India)", 
        "nl-NL": "Dutch (Netherlands)", 
        "ne-NP": "Nepali (Nepal)", 
        "nb-NO": "Norwegian Bokmal (Norway)", 
        "pl-PL": "Polish (Poland)", 
        "pt-BR": "Portuguese (Brazil)", 
        "pt-PT": "Portuguese (Portugal)", 
        "ro-RO": "Romanian (Romania)", 
        "si-LK": "Sinhala (Sri Lanka)", 
        "sk-SK": "Slovak (Slovakia)", 
        "sl-SI": "Slovenian (Slovenia)", 
        "su-ID": "Sundanese (Indonesia)", 
        "sw-TZ": "Swahili (Tanzania)", 
        "sw-KE": "Swahili (Kenya)", 
        "fi-FI": "Finnish (Finland)", 
        "sv-SE": "Swedish (Sweden)", 
        "ta-IN": "Tamil (India)", 
        "ta-SG": "Tamil (Singapore)", 
        "ta-LK": "Tamil (Sri Lanka)", 
        "ta-MY": "Tamil (Malaysia)", 
        "te-IN": "Telugu (India)", 
        "vi-VN": "Vietnamese (Vietnam)", 
        "tr-TR": "Turkish (Turkey)", 
        "ur-PK": "Urdu (Pakistan)", 
        "ur-IN": "Urdu (India)", 
        "el-GR": "Greek (Greece)", 
        "bg-BG": "Bulgarian (Bulgaria)", 
        "ru-RU": "Russian (Russia)", 
        "sr-RS": "Serbian (Serbia)", 
        "uk-UA": "Ukrainian (Ukraine)", 
        "he-IL": "Hebrew (Israel)", 
        "ar-IL": "Arabic (Israel)", 
        "ar-JO": "Arabic (Jordan)", 
        "ar-AE": "Arabic (United)", 
        "ar-BH": "Arabic (Bahrain)", 
        "ar-DZ": "Arabic (Algeria)", 
        "ar-SA": "Arabic (Saudi)", 
        "ar-IQ": "Arabic (Iraq)", 
        "ar-KW": "Arabic (Kuwait)", 
        "ar-MA": "Arabic (Morocco)", 
        "ar-TN": "Arabic (Tunisia)", 
        "ar-OM": "Arabic (Oman)", 
        "ar-PS": "Arabic (Palestine)", 
        "ar-QA": "Arabic (Qatar)", 
        "ar-LB": "Arabic (Lebanon)", 
        "ar-EG": "Arabic (Egypt)", 
        "fa-IR": "Persian (Iran)", 
        "hi-IN": "Hindi (India)", 
        "th-TH": "Thai (Thailand)", 
        "ko-KR": "Korean (South Korea)", 
        "jp-JP": "Japanese (Japan)", 
        "cmn-Hant-TW": "Mandarin Chinese (Taiwan)", 
        "yue-Hant-HK": "Cantonese Chinese (Hong", 
        "cmn-Hans-HK": "Mandarin Chinese (Hong", 
        "cmn-Hans-CN": "Mandarin Chinese (China)"
}
        
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/dev/Analysis-66668883776.json" # Change this to your key.json
category = {0: 'Unknown', 1: 'Very Unlikely', 2: 'Unlikely', 3: 'Possible', 4: 'Likely', 5: 'Very Likely'}

if __name__ == '__main__':
    print()
    prompt = GooglePrompt()
    prompt.prompt = '> '
    prompt.cmdloop('\nThey\'ve done studies you know. Sixty percent of the time it works every time....')

    ## FUTURE WORK
    #     1. Generate a log file once the application is started that documents
    #        all commands and output
    #     2. Create a config file for the global variables
    #     3. Sent all output to a NoSQL database
    #        a. All documents linked
    #        b. Link key words to documents / files
    #     4. Create a do_query that allows you to search all output
    #        a. Show the files, text, etc related to the query

            
            
