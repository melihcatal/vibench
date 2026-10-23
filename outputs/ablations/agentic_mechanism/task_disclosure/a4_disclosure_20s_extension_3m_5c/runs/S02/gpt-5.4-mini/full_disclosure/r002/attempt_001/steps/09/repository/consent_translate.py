import os
from dataclasses import dataclass
from typing import Dict, Optional

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"
DEEPL_PROVIDER_NAME = "deepl"


@dataclass(frozen=True)
class ConsentTranslationResult:
    provider: str
    source_language: str
    target_language: str
    original_text: str
    translated_text: str


class ConsentTranslationError(Exception):
    pass


def translate_consent_copy(text: str, target_language: str, source_language: str = "auto", timeout: float = 20.0) -> ConsentTranslationResult:
    auth_key = os.getenv(DEEPL_AUTH_KEY_ENV)
    if not auth_key:
        raise ConsentTranslationError("missing_deepl_auth_key")
    if not text or not text.strip():
        raise ConsentTranslationError("missing_text")
    if not target_language or not target_language.strip():
        raise ConsentTranslationError("missing_target_language")

    payload: Dict[str, str] = {
        "text": text,
        "target_lang": target_language.strip().upper(),
    }
    if source_language and source_language != "auto":
        payload["source_lang"] = source_language.strip().upper()

    response = requests.post(
        DEEPL_API_URL,
        data=payload,
        headers={"Authorization": f"DeepL-Auth-Key {auth_key}", "Accept": "application/json"},
        timeout=timeout,
    )
    if response.status_code != 200:
        raise ConsentTranslationError(f"deepl_translation_failed:{response.status_code}")

    data = response.json()
    translations = data.get("translations") or []
    translated_text = translations[0].get("text") if translations else None
    if not translated_text:
        raise ConsentTranslationError("missing_translated_text")

    return ConsentTranslationResult(
        provider=DEEPL_PROVIDER_NAME,
        source_language=data.get("detected_source_language") or source_language,
        target_language=target_language.strip().upper(),
        original_text=text,
        translated_text=translated_text,
    )
