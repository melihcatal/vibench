from typing import Dict, Any
import os
from google.cloud import translate_v2 as translate


def translate_compliance_note(text: str, target_language: str) -> Dict[str, Any]:
    """Translates encryption or compliance notes using Google Cloud Translation API."""
    client = translate.Client()

    result = client.translate(text, target_language=target_language, format_="text")

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "model": "google-translate-v2",
    }
