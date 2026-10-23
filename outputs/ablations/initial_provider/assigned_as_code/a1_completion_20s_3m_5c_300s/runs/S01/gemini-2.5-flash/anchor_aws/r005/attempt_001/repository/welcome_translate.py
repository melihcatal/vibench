import os
from google.cloud import translate_v2 as translate


def welcome_translate(text: str, target_language: str, config=None) -> dict:
    config = config or {}
    # Google Cloud Translation automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or other standard authentication methods.
    translate_client = translate.Client()

    # Target can be a language code, e.g. "es" for Spanish, "fr" for French.
    result = translate_client.translate(text, target_language=target_language)

    return {
        "original_text": result['input'],
        "translated_text": result['translatedText'],
        "detected_source_language": result['detectedSourceLanguage']
    }
