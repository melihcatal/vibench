import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str) -> str:
    """
    Translates text to a target language using Google Cloud Translate.

    Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment
    for a service account with the "Cloud Translation API User" role.
    """
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    
    return result['translatedText']
