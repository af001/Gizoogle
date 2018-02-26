#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 22:35:41 2018

@author: devnet
"""
import os

class Config():
    
    # Google Cloud Console API Key - Load
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/devnet/Downloads/Analysis-666680c8f996.json"
        
    # Google Project ID
    PROJECT_ID = 'analysis-194418'
    
    # Project path for saving log files
    PROJECT_PATH = '/home/devnet/analysis'
    
    # Google storage buckets
    IMAGE_STORAGE_BUCKET = 'image_dump_0'
    AUDIO_STORAGE_BUCKET = 'speech_dump_0'
    DOCUMENT_STORAGE_BUCKET = 'document_dump_0'
    VIDEO_STORAGE_BUCKET = 'video_dump_0'
    
    # Max content length
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    
    # Allowed file extensions for file uploads
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'flac', 'txt', 'mov', 'mp4', 'mpeg4', 'avi'])
    
    # Classification categories
    CATEGORY = {0: 'Unknown', 1: 'Very Unlikely', 2: 'Unlikely', 3: 'Possible', 4: 'Likely', 5: 'Very Likely'}
    
    # Available languages for speech transcriptions 
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
