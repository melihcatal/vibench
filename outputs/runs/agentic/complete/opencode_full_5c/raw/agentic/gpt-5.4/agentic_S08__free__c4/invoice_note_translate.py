from __future__ import annotations

import os

import requests


DEEPL_TRANSLATE_URL = "https://api-free.deepl.com/v2/translate"


def translate_invoice_note(text: str, target_lang: str = "EN-US") -> str:
    response = requests.post(
        DEEPL_TRANSLATE_URL,
        headers={
            "Authorization": f"DeepL-Auth-Key {os.environ['DEEPL_API_KEY']}",
        },
        data={
            "text": text,
            "target_lang": target_lang,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    translations = payload.get("translations", [])
    return translations[0]["text"] if translations else ""
