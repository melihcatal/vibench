from typing import Dict
from google.cloud import translate_v2 as translate
import os


def translate_appeal_text(text: str, target_language: str = "en") -> Dict:
    """Translate appeal text for review using Google Cloud Translation."""
    client = translate.Client()

    result = client.translate(text, target_language=target_language, format_="text")

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }
