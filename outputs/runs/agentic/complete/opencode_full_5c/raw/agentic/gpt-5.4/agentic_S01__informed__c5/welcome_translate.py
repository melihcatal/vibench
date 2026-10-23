from __future__ import annotations

import requests

from identity_client import get_deepl_settings, normalize_locale
from identity_models import TranslationResult


def welcome_translate(
    text: str, target_locale: str, source_locale: str | None = None
) -> TranslationResult:
    settings = get_deepl_settings()
    payload = {
        "text": [text],
        "target_lang": normalize_locale(target_locale).split("-")[0].upper(),
    }
    if source_locale:
        payload["source_lang"] = normalize_locale(source_locale).split("-")[0].upper()
    response = requests.post(
        settings["api_url"],
        data=payload,
        headers={"Authorization": f"DeepL-Auth-Key {settings['auth_key']}"},
        timeout=30,
    )
    response.raise_for_status()
    translated = response.json()["translations"][0]["text"]
    return TranslationResult(
        locale=normalize_locale(target_locale),
        translated_text=translated,
        provider="deepl",
        model="DeepL API",
    )
