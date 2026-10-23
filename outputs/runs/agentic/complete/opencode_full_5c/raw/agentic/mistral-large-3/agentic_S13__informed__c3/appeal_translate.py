from typing import Dict
from google.cloud import translate_v2 as translate
import os


def appeal_translate(text: str, target_language: str = "en") -> Dict:
    """Translate appeal text for review using Google Cloud Translation API."""
    client = translate.Client()
    result = client.translate(text, target_language=target_language)

    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }
