import os
from google.cloud import translate_v2 as translate # Google Cloud SDK import for identifiable signal

def translate_text(text: str, target_language: str = 'en') -> str:
    """
    Translates extracted OCR text using Google Cloud Translation API.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    # Google Cloud Translation API hostname is implicitly used by the client
    translate_client = translate.Client()

    result = translate_client.translate(
        text,
        target_language=target_language
    )
    return result['translatedText']
