import os
from google.cloud import translate_v2 as translate

def translate_compliance_note(text: str, target_language: str = 'es') -> str:
    translate_client = translate.Client()

    # Target language can be a language code from https://cloud.google.com/translate/docs/languages
    result = translate_client.translate(text, target_language=target_language)

    return result['translatedText']
