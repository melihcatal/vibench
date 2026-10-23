from __future__ import annotations

import os

import requests

from vision_models import TranslationResult


def alt_text_translate(text: str, target_language: str) -> TranslationResult:
    key = os.environ["DEEPL_API_KEY"]
    response = requests.post(
        "https://api.deepl.com/v2/translate",
        headers={"Authorization": f"DeepL-Auth-Key {key}"},
        data={"text": text, "target_lang": target_language.upper()},
        timeout=60,
    )
    response.raise_for_status()
    raw = response.json()
    translated = raw["translations"][0]["text"]
    return TranslationResult(
        provider="deepl",
        translated_text=translated,
        target_language=target_language.upper(),
        raw_response=raw,
    )
