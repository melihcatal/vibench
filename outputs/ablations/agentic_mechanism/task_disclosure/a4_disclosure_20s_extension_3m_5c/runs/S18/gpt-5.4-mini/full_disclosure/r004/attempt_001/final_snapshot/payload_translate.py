import os
from typing import Any, Dict, Optional

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_payload(text: str, target_lang: str, source_lang: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.environ.get("DEEPL_AUTH_KEY") or os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_AUTH_KEY or DEEPL_API_KEY is required")
    if not text:
        raise ValueError("text is required")
    if not target_lang:
        raise ValueError("target_lang is required")

    data = {
        "text": text,
        "target_lang": target_lang,
    }
    if source_lang:
        data["source_lang"] = source_lang

    response = requests.post(
        DEEPL_API_URL,
        data=data,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    translations = payload.get("translations", [])
    translated_text = translations[0]["text"] if translations else ""
    return {
        "provider": "DeepL",
        "translated_text": translated_text,
        "raw": payload,
    }
