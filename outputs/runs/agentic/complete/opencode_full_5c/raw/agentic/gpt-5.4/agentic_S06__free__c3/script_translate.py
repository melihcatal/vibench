from __future__ import annotations

import os

import requests


def translate_script(
    text: str, target_language: str, source_language: str | None = None
) -> str:
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPL_API_KEY is required for DeepL translation")
    payload = {"text": [text], "target_lang": target_language}
    if source_language:
        payload["source_lang"] = source_language
    response = requests.post(
        "https://api.deepl.com/v2/translate",
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        data=payload,
        timeout=30,
    )
    response.raise_for_status()
    body = response.json()
    return body["translations"][0]["text"]
