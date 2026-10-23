import os
from google.cloud import translate_v2 as translate

def translate_consent_text(text: str, target_language: str) -> str:
    """
    Translates consent screen text using Google Cloud Translation API.

    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)
    
    print(f"Text: {result['input']}")
    print(f"Translation: {result['translatedText']}")
    print(f"Detected source language: {result['detectedSourceLanguage']}")

    return result["translatedText"]
