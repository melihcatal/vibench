from __future__ import annotations

import os
from typing import Dict, List

import requests

from document_models import normalize_sections


def translate_ocr_text(text: str, target_language: str) -> Dict[str, List[str]]:
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("Missing required environment variable: DEEPL_API_KEY")
    sections = normalize_sections(text)
    response = requests.post(
        "https://api.deepl.com/v2/translate",
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        data={"target_lang": target_language, "text": sections},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    translated = [item["text"] for item in payload.get("translations", [])]
    return {"provider": ["deepl"], "translations": translated}
