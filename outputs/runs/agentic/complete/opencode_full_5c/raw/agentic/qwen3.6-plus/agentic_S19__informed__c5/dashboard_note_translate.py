from __future__ import annotations

import os
from typing import Any

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_dashboard_note(
    text: str,
    target_lang: str = "ES",
    source_lang: str | None = None,
) -> dict[str, Any]:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    headers = {
        "Authorization": f"DeepL-Auth-Key {auth_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {
        "text": text,
        "target_lang": target_lang,
    }
    if source_lang:
        payload["source_lang"] = source_lang
    resp = requests.post(DEEPL_API_URL, headers=headers, data=payload, timeout=30)
    resp.raise_for_status()
    body = resp.json()
    translations = body.get("translations", [])
    translated_texts = [t.get("text", "") for t in translations]
    detected_source = (
        translations[0].get("detected_source_language", "") if translations else ""
    )
    return {
        "original_text": text,
        "translated_text": translated_texts[0] if translated_texts else "",
        "source_lang": detected_source,
        "target_lang": target_lang,
        "service": "DeepL API",
    }
