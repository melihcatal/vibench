import os
from typing import Any, Dict

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def _translate_text(text: str, target_lang: str, source_lang: str | None = None) -> str:
    api_key = os.environ.get("DEEPL_AUTH_KEY") or os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise RuntimeError("Missing DEEPL_AUTH_KEY or DEEPL_API_KEY")

    payload = {"text": text, "target_lang": target_lang.upper()}
    if source_lang:
        payload["source_lang"] = source_lang.upper()

    response = requests.post(
        DEEPL_API_URL,
        data=payload,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    translations = data.get("translations", [])
    if not translations:
        raise RuntimeError("DeepL returned no translations")
    return translations[0]["text"]


def translate_record_fields(record: Dict[str, Any], target_lang: str, source_lang: str | None = None) -> Dict[str, Any]:
    translated = dict(record)
    for field in ("title", "summary", "description", "body"):
        value = translated.get(field)
        if isinstance(value, str) and value.strip():
            translated[field] = _translate_text(value, target_lang, source_lang)
    return translated


def translate_record(record: Dict[str, Any], target_lang: str, source_lang: str | None = None) -> Dict[str, Any]:
    return translate_record_fields(record, target_lang, source_lang)
