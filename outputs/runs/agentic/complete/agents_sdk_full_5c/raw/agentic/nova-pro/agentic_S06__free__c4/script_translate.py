import os
from google.cloud import translate

def translate_text(text, target_language):
    client = translate.TranslateClient()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']