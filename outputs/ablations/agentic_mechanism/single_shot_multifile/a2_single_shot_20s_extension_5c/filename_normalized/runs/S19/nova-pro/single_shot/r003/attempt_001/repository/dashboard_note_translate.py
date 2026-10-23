import os
from google.cloud import translate_v2 as translate

def translate_note(text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']