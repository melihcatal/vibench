import os
from google.cloud import translate_v2 as translate

def welcome_translate(text: str, target_language: str) -> dict:
    # Google Cloud Translation API client initialization
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    translate_client = translate.Client()

    # Translate the text
    result = translate_client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "original_text": result["input"],
        "detected_source_language": result["detectedSourceLanguage"]
    }
