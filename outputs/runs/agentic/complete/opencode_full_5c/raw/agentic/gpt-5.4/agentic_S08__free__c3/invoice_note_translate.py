from __future__ import annotations

import os

import requests


DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_API_URL = os.getenv("DEEPL_API_URL", "https://api.deepl.com/v2/translate")


def invoice_note_translate(text: str, target_language: str = "EN") -> str:
    if not DEEPL_API_KEY:
        raise ValueError("DEEPL_API_KEY is required")
    response = requests.post(
        DEEPL_API_URL,
        headers={"Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"},
        data={"text": text, "target_lang": target_language},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    translations = data.get("translations", [])
    if not translations:
        return ""
    return translations[0].get("text", "")
