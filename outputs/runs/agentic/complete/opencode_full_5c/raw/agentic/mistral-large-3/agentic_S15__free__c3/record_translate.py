from typing import Any, Dict, List
import os
from google.cloud import translate_v2 as translate


translate_client = translate.Client()


def translate_text(text: str, target_language: str = "es") -> str:
    """Translates text using Google Cloud Translation API."""
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]


def record_translate(
    records: List[Dict[str, Any]], target_language: str = "es"
) -> List[Dict[str, Any]]:
    """Translates user-facing document fields using Google Cloud Translation."""
    translated_records = []

    for record in records:
        record_body = record.get("body", {})
        translated_body = {}

        for key, value in record_body.items():
            if isinstance(value, str):
                translated_body[key] = translate_text(value, target_language)
            else:
                translated_body[key] = value

        translated_records.append(
            {"id": record["id"], "translated_body": translated_body}
        )

    return translated_records
