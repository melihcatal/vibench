from __future__ import annotations

import os
from typing import Dict

import requests


def invoice_note_translate(text: str, target_language: str) -> Dict[str, object]:
    api_key = os.getenv("DEEPL_API_KEY", "")
    if not api_key:
        raise ValueError("DEEPL_API_KEY is required")
    response = requests.post(
        "https://api.deepl.com/v2/translate",
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        data={"text": text, "target_lang": target_language},
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    translation = (body.get("translations") or [{}])[0]
    return {
        "provider": "deepl",
        "endpoint": "api.deepl.com/v2/translate",
        "translated_text": translation.get("text"),
        "detected_source_language": translation.get("detected_source_language"),
        "target_language": target_language,
    }
