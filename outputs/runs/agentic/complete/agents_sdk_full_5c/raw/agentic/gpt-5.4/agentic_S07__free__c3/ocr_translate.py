from __future__ import annotations

import os

from google.cloud import translate_v2 as translate

from document_models import TextExtractionResult


def translate_ocr_text(result: TextExtractionResult, target_language: str, source_language: str | None = None) -> dict:
    client = translate.Client()
    response = client.translate(
        result.text,
        target_language=target_language,
        source_language=source_language,
        format_="text",
    )
    return {
        "provider": "google_cloud_translate",
        "project": os.getenv("GOOGLE_CLOUD_PROJECT"),
        "translated_text": response["translatedText"],
        "detected_source_language": response.get("detectedSourceLanguage"),
    }
