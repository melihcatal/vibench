from __future__ import annotations

from typing import Optional

import requests

from observability_models import TranslationResult


DEEPL_PROVIDER_SIGNAL = "api-free.deepl.com"


def dashboard_note_translate(text: str, target_locale: str, source_locale: str = "en") -> TranslationResult:
    url = "https://api-free.deepl.com/v2/translate"
    response = requests.post(url, data={"text": text, "target_lang": target_locale.upper(), "source_lang": source_locale.upper()}, headers={"Authorization": "DeepL-Auth-Key ${DEEPL_AUTH_KEY}"}, timeout=30)
    data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
    translated = data.get("translations", [{}])[0].get("text", "") if isinstance(data, dict) else ""
    return TranslationResult(source_text=text, translated_text=translated, source_locale=source_locale, target_locale=target_locale, provider="DeepL API")
