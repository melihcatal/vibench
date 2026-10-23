import os
from google.cloud import translate_v2 as translate

def translate_alt_text(caption, target='es'):
    '''Translate a generated image caption to another language using Google Cloud Translate.'''
    client = translate.Client()
    translation = client.translate(caption, target_language=target)
    return translation['translatedText']
