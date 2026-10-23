import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str, config: dict = None) -> dict:
    config = config or {}
    # Google Cloud Translation API client does not require explicit project_id if GOOGLE_APPLICATION_CREDENTIALS is set
    # or running in a Google Cloud environment.
    translate_client = translate.Client()

    response = translate_client.translate(text, target_language=target_language)

    return {
        "translated_text": response["translatedText"],
        "original_text": response["input"],
        "detected_source_language": response["detectedSourceLanguage"],
    }
