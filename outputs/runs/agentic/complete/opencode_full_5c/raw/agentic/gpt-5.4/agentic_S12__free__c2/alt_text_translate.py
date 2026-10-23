from __future__ import annotations

import json
import os

import requests


DEEPL_API_URL = "https://api.deepl.com/v2/translate"


def alt_text_translate(text: str, target_language: str) -> str:
    api_key = os.environ["DEEPL_API_KEY"]
    response = requests.post(
        DEEPL_API_URL,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        data={"text": text, "target_lang": target_language},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    translations = data.get("translations", [])
    if not translations:
        return ""
    return str(translations[0].get("text", "")).strip()
