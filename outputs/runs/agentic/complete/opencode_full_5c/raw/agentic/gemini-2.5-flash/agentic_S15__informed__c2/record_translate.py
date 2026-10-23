import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any


def translate_document_field(text: str, target_language: str) -> Dict[str, Any]:
    """
    Translates user-facing document fields using Google Cloud Translation.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }
