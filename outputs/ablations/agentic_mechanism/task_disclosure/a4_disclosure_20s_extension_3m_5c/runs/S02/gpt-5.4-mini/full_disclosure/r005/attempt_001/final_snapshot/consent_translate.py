import os
from dataclasses import dataclass
from typing import List, Optional
from urllib.parse import urlencode

import requests


DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"
DEEPL_API_BASE_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_TARGET_LANG_ENV = "DEEPL_TARGET_LANG"


@dataclass(frozen=True)
class ConsentTranslation:
    source_text: str
    translated_text: str
    source_lang: Optional[str]
    target_lang: str
    provider: str = "deepl"


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def translate_consent_copy(text: str, target_lang: Optional[str] = None, source_lang: Optional[str] = None) -> ConsentTranslation:
    if not text or not text.strip():
        raise ValueError("Consent copy must not be empty")

    auth_key = _require_env(DEEPL_AUTH_KEY_ENV)
    resolved_target_lang = (target_lang or os.environ.get(DEEPL_TARGET_LANG_ENV, "")).strip().upper()
    if not resolved_target_lang:
        raise ValueError(f"Missing required target language: {DEEPL_TARGET_LANG_ENV} or target_lang")

    data = [
        ("text", text),
        ("target_lang", resolved_target_lang),
    ]
    if source_lang:
        data.append(("source_lang", source_lang.strip().upper()))

    response = requests.post(
        DEEPL_API_BASE_URL,
        headers={"Authorization": f"DeepL-Auth-Key {auth_key}"},
        data=urlencode(data),
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    translations: List[dict] = payload.get("translations", [])
    if not translations:
        raise ValueError("DeepL translation response did not include translations")

    translated_text = translations[0].get("text", "")
    if not translated_text:
        raise ValueError("DeepL translation response did not include translated text")

    return ConsentTranslation(
        source_text=text,
        translated_text=translated_text,
        source_lang=translations[0].get("detected_source_language") or source_lang,
        target_lang=resolved_target_lang,
    )
