from __future__ import annotations

import os
from typing import Optional

import requests

from speech_models import TranslationResult

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_script(text: str, target_language: str, source_language: Optional[str] = None) -> TranslationResult:
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY is required")
    payload = {
        "text": [text],
        "target_lang": target_language,
    }
    if source_language:
        payload["source_lang"] = source_language
    response = requests.post(
        DEEPL_API_URL,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    item = response.json()["translations"][0]
    return TranslationResult(
        provider="deepl",
        translated_text=item["text"],
        detected_source_language=item.get("detected_source_language"),
    )
