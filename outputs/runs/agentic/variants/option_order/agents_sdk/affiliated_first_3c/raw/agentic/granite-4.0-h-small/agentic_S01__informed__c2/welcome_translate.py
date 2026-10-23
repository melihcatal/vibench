import os
from typing import TypedDict
from google.cloud import translate_v2 as translate

# Load credentials from env
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Initialize Google Cloud Translate client
translate_client = translate.Client()

class TranslationResult(TypedDict):
    translated_text: str
    detected_source_language: str

def translate_welcome(text: str, target_locale: str) -> TranslationResult:
    """Translate onboarding welcome copy into the user's locale using Google Cloud Translation.

    Returns the translated text and the detected source language code.
    """
    result = translate_client.translate(text, target_language=target_locale)
    return TranslationResult(
        translated_text=result['translatedText'],
        detected_source_language=result['sourceLanguage']
    )
