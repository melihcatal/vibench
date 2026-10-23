import os
import json
from typing import Dict, Any
from google.cloud import translate_v2 as translate


def translate_compliance_note(text: str, target_language: str = "en") -> Dict[str, Any]:
    client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "original_text": text,
        "source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
        "key_id": os.getenv("GOOGLE_KMS_KEY_NAME"),
        "model": "google-translate-v2",
    }


def batch_translate_notes(notes: list, target_language: str = "en") -> list:
    client = translate.Client()
    results = client.translate(notes, target_language=target_language)

    return [
        {
            "translated_text": result["translatedText"],
            "original_text": result["input"],
            "source_language": result["detectedSourceLanguage"],
            "target_language": target_language,
            "key_id": os.getenv("GOOGLE_KMS_KEY_NAME"),
            "model": "google-translate-v2",
        }
        for result in results
    ]
