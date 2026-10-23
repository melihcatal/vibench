from __future__ import annotations

import requests

from safety_client import get_deepl_base_url, get_deepl_headers
from safety_models import TranslationResult


def appeal_translate(text: str, target_language: str = "EN") -> TranslationResult:
    response = requests.post(
        f"{get_deepl_base_url()}/translate",
        headers=get_deepl_headers(),
        json={"text": [text], "target_lang": target_language},
        timeout=30,
    )
    response.raise_for_status()
    body = response.json()
    translated = body["translations"][0]["text"]
    return TranslationResult(
        translated_text=translated,
        to_language=target_language,
        provider="DeepL",
    )
