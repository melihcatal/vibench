from __future__ import annotations

import os
from typing import Optional

import requests

from security_client import DEFAULT_DEEPL_MODEL_TYPE
from security_models import TranslationResult


DEEPL_API_URL = "https://api.deepl.com/v2/translate"


def compliance_note_translate(text: str, target_language: str, source_language: Optional[str] = None) -> TranslationResult:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    payload = {
        "text": [text],
        "target_lang": target_language,
        "model_type": DEFAULT_DEEPL_MODEL_TYPE,
    }
    if source_language:
        payload["source_lang"] = source_language
    response = requests.post(
        DEEPL_API_URL,
        data=payload,
        headers={"Authorization": f"DeepL-Auth-Key {auth_key}"},
        timeout=30,
    )
    response.raise_for_status()
    body = response.json()
    translation = body["translations"][0]
    return TranslationResult(
        provider="deepl",
        source_language=translation.get("detected_source_language", source_language),
        target_language=target_language,
        translated_text=translation["text"],
    )


def run(text: str, target_language: str, source_language: Optional[str] = None) -> dict:
    result = compliance_note_translate(text, target_language, source_language)
    return result.__dict__
