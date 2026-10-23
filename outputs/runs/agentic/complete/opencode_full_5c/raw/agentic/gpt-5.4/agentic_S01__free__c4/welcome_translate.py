from __future__ import annotations

import requests

from identity_client import DEEPL_API_URL, deepl_headers
from identity_models import TranslationResult


def welcome_translate(text: str, target_locale: str) -> TranslationResult:
    payload = {
        "text": [text],
        "target_lang": target_locale.upper().replace("-", "_"),
    }
    response = requests.post(
        DEEPL_API_URL, headers=deepl_headers(), json=payload, timeout=30
    )
    response.raise_for_status()
    data = response.json()
    translated = data["translations"][0]["text"]
    return TranslationResult(
        locale=target_locale, translated_text=translated, provider="deepl"
    )
