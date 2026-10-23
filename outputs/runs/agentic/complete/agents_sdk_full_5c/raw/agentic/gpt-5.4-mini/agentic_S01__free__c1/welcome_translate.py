from __future__ import annotations

import os

import requests

# DeepL hosted translation API
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def welcome_translate(text: str, target_locale: str) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY", "")
    resp = requests.post(
        DEEPL_API_URL,
        data={"auth_key": auth_key, "text": text, "target_lang": target_locale.upper()},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["translations"][0]["text"]
