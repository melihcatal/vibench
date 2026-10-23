from __future__ import annotations

import os

import requests

DEEPL_API_HOST = "https://api-free.deepl.com/v2/translate"


def appeal_translate(text: str, target_language: str = "EN-US") -> dict:
    auth_key = os.getenv("DEEPL_AUTH_KEY", "")
    response = requests.post(
        DEEPL_API_HOST,
        data={"auth_key": auth_key, "text": text, "target_lang": target_language},
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    translated = data.get("translations", [{}])[0].get("text", text)
    return {"provider": "DeepL", "target_language": target_language, "translated_text": translated}
