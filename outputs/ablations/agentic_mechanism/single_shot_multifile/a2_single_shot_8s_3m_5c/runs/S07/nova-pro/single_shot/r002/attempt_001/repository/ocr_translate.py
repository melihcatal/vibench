import os
from google.cloud import translate_v2 as translate

translate_client = translate.Client()

def translate_text(text, target_language='en'):
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']