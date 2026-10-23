from __future__ import annotations

from document_client import (
    GOOGLE_TRANSLATE_API_URL,
    build_google_query_params,
    build_google_vision_headers,
    post_json,
)
from document_models import TranslationResult


def translate_ocr_text(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    payload = {"q": text, "target": target_language, "format": "text"}
    if source_language:
        payload["source"] = source_language
    response_json = post_json(
        GOOGLE_TRANSLATE_API_URL,
        payload,
        headers=build_google_vision_headers(),
        params=build_google_query_params("GOOGLE_CLOUD_API_KEY"),
    )
    translations = response_json.get("data", {}).get("translations", [])
    first = translations[0] if translations else {}
    return TranslationResult(
        provider="google-cloud-translate",
        translated_text=first.get("translatedText", ""),
        detected_language=first.get("detectedSourceLanguage"),
        raw_response=response_json,
    )
