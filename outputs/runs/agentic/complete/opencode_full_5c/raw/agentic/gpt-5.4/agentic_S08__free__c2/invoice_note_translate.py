from __future__ import annotations

import os

import requests


DEEPL_TRANSLATE_URL = "https://api.deepl.com/v2/translate"


def translate_invoice_note(
    text: str, target_language: str = "EN-US", source_language: str | None = None
) -> str:
    payload = {
        "text": [text],
        "target_lang": target_language,
    }
    if source_language:
        payload["source_lang"] = source_language
    response = requests.post(
        DEEPL_TRANSLATE_URL,
        headers={
            "Authorization": f"DeepL-Auth-Key {os.environ['DEEPL_API_KEY']}",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["translations"][0]["text"]
