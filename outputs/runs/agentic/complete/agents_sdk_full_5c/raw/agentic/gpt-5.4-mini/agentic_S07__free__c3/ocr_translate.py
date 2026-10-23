from __future__ import annotations

import os

from google.cloud import translate_v3

from document_models import normalize_text

TRANSLATION_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "")
TRANSLATION_LOCATION = os.getenv("TRANSLATE_LOCATION", "global")


def translate_ocr_text(text: str, target_language: str = "en") -> str:
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{TRANSLATION_PROJECT_ID}/locations/{TRANSLATION_LOCATION}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [normalize_text(text)],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    return response.translations[0].translated_text if response.translations else ""
