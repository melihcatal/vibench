from __future__ import annotations

import os

import requests


DEEPL_API_URL = "https://api.deepl.com/v2/translate"


def appeal_translate(text: str, target_lang: str = "EN-US", source_lang: str | None = None) -> str:
    auth_key = os.environ["DEEPL_API_KEY"]
    data = {
        "text": text,
        "target_lang": target_lang,
    }
    if source_lang:
        data["source_lang"] = source_lang
    response = requests.post(
        DEEPL_API_URL,
        headers={"Authorization": f"DeepL-Auth-Key {auth_key}"},
        data=data,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["translations"][0]["text"]
