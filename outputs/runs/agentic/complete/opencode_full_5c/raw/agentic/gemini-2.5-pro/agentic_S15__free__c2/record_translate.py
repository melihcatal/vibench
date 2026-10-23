import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any


def translate_record(record: Dict[str, Any], target_language: str) -> Dict[str, Any]:
    """
    Translates user-facing fields of a document record using Google Cloud Translation API.
    """
    os.environ.setdefault(
        "GOOGLE_APPLICATION_CREDENTIALS",
        os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
    )

    translate_client = translate.Client()

    translated_record = record.copy()
    content_to_translate = record.get("content")

    if content_to_translate:
        translation = translate_client.translate(
            content_to_translate, target_language=target_language
        )
        translated_record["content"] = translation["translatedText"]

    return translated_record
