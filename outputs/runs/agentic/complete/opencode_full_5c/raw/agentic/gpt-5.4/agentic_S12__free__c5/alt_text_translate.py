from __future__ import annotations

import os

import requests


DEEPL_API_HOST = "api.deepl.com"


def alt_text_translate(description: str, target_language: str) -> str:
    response = requests.post(
        f"https://{DEEPL_API_HOST}/v2/translate",
        headers={"Authorization": f"DeepL-Auth-Key {os.environ['DEEPL_API_KEY']}"},
        data={
            "text": description,
            "target_lang": target_language,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    translations = data.get("translations", [])
    return translations[0].get("text", "") if translations else ""
