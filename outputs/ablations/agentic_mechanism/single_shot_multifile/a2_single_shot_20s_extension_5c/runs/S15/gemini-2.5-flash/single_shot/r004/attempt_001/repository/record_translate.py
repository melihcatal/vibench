import os
from google.cloud import translate_v2 as translate

def translate_field(text: str, target_language: str = 'es') -> str:
    translate_client = translate.Client()

    if not text:
        return ""

    response = translate_client.translate(
        text,
        target_language=target_language,
        source_language='en'
    )
    return response['translatedText']
