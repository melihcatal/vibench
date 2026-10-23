import os
from google.cloud import translate_v2 as translate


def stored_text_translate(text: str, target_language: str = 'en') -> str:
    client = translate.Client()
    response = client.translate(text, target_language=target_language)
    return response['translatedText']
