from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


def dashboard_note_translate(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    session: Optional[requests.Session] = None,
) -> Dict[str, Any]:
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("Missing DEEPL_API_KEY")
    http = session or requests.Session()
    payload = {
        "text": [text],
        "target_lang": target_language.upper(),
    }
    if source_language:
        payload["source_lang"] = source_language.upper()
    response = http.post(
        "https://api-free.deepl.com/v2/translate",
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    body = response.json()
    translations = body.get("translations", [])
    if not translations:
        raise ValueError("DeepL returned no translations")
    translation = translations[0]
    return {
        "provider": "DeepL",
        "translated_text": translation.get("text"),
        "detected_source_language": translation.get("detected_source_language"),
        "target_language": target_language.upper(),
    }
