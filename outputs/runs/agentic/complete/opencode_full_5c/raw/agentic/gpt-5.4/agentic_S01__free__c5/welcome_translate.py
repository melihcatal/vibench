from __future__ import annotations

import os

import requests


DEEPL_API_URL = "https://api.deepl.com/v2/translate"
DEEPL_AUTH_ENV = "DEEPL_API_KEY"


def welcome_translate(text: str, target_locale: str) -> dict:
    api_key = os.environ[DEEPL_AUTH_ENV]
    response = requests.post(
        DEEPL_API_URL,
        data={"text": text, "target_lang": target_locale.upper()},
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    translations = payload.get("translations", [])
    translated_text = translations[0]["text"] if translations else ""
    return {
        "provider": "deepl",
        "target_locale": target_locale,
        "translated_text": translated_text,
        "raw": payload,
    }
