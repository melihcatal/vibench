from __future__ import annotations

from identity_client import load_config
from identity_models import TranslationResult

import requests


def welcome_translate(text: str, target_locale: str) -> TranslationResult:
    config = load_config()
    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        data={
            "auth_key": config.deepl_api_key,
            "text": text,
            "target_lang": target_locale.upper(),
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    item = payload["translations"][0]
    return TranslationResult(
        translated_text=item["text"],
        detected_language=item.get("detected_source_language"),
        raw=payload,
    )
