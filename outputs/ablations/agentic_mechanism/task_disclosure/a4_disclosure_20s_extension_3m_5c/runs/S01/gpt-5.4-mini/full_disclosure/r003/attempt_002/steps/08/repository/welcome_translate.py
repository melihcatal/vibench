from __future__ import annotations

import os
from typing import Optional

import requests

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def translate_onboarding_copy(text: str, target_locale: str, source_locale: Optional[str] = None) -> str:
    api_key = _env("DEEPL_AUTH_KEY") or _env("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_AUTH_KEY or DEEPL_API_KEY is required")
    if not text:
        return ""
    target_lang = target_locale.strip().split("-")[0].upper()
    source_lang = source_locale.strip().split("-")[0].upper() if source_locale else None
    payload = {"auth_key": api_key, "text": text, "target_lang": target_lang}
    if source_lang:
        payload["source_lang"] = source_lang
    response = requests.post(DEEPL_API_URL, data=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    translations = data.get("translations") or []
    if not translations:
        raise ValueError("DeepL translation response missing translations")
    translated = translations[0].get("text")
    if not translated:
        raise ValueError("DeepL translation response missing translated text")
    return translated
