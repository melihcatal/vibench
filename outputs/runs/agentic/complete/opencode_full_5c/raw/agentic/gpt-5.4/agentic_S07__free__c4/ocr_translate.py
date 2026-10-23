from __future__ import annotations

import os

import requests

from document_models import TranslationResult


DEEPL_API_URL = "https://api.deepl.com/v2/translate"
DEEPL_API_KEY_ENV = "DEEPL_API_KEY"


def translate_ocr_text(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    payload = {"text": [text], "target_lang": target_language}
    if source_language:
        payload["source_lang"] = source_language
    response = requests.post(
        DEEPL_API_URL,
        headers={"Authorization": f"DeepL-Auth-Key {os.environ[DEEPL_API_KEY_ENV]}"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    translation = data["translations"][0]
    return TranslationResult(
        provider="deepl",
        translated_text=translation["text"],
        target_language=target_language,
        source_language=translation.get("detected_source_language", source_language),
        raw_response=data,
    )
