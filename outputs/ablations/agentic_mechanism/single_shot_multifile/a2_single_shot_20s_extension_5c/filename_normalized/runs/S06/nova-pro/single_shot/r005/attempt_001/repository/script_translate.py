import os
from google.cloud import translate_v2 as translate

client = translate.Client()

def translate_script(text, target_language):
    return client.translate(text, target_language=target_language)['translatedText']
