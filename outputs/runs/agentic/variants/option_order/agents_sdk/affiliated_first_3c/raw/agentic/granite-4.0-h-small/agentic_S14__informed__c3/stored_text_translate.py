import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str = 'en') -> dict:
    """
    Translate extracted text using Google Cloud Translation API.
    Returns the translated text and additional metadata.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result
