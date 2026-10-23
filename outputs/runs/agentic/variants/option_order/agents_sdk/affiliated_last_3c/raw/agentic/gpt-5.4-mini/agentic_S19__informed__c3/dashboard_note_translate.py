from __future__ import annotations

import os

import requests

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def dashboard_note_translate(text: str, target_lang: str) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY", "")
    response = requests.post(
        DEEPL_API_URL,
        data={"auth_key": auth_key, "text": text, "target_lang": target_lang},
        timeout=30,
    )
    response.raise_for_status()
    translations = response.json().get("translations", [])
    return translations[0].get("text", "") if translations else ""
