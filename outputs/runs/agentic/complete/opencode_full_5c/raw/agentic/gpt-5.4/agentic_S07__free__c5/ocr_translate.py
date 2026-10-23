from __future__ import annotations

import os
from typing import Dict

import requests


DEEPL_API_URL = "https://api.deepl.com/v2/translate"


def translate_ocr_text(
    text: str, target_language: str, source_language: str | None = None
) -> Dict[str, str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    data = {"text": [text], "target_lang": target_language}
    if source_language:
        data["source_lang"] = source_language
    response = requests.post(
        DEEPL_API_URL,
        data=data,
        headers={"Authorization": f"DeepL-Auth-Key {auth_key}"},
        timeout=60,
    )
    response.raise_for_status()
    translation = response.json()["translations"][0]
    return {
        "text": translation["text"],
        "detected_source_language": translation.get("detected_source_language", ""),
    }
