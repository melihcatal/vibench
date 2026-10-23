"""
record_translate.py - Translate user-facing document fields
using the DeepL Translation API.

Provider: DeepL API (api.deepl.com) - concrete model: deepl-translate
"""

import os
from typing import Any, Dict, List, Optional

import requests

from database_models import DocumentRecord, extract_user_facing_fields

# DeepL provider-specific configuration
DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY", "")
DEEPL_API_URL = os.environ.get("DEEPL_API_URL", "https://api.deepl.com/v2/translate")
DEEPL_MODEL_ID = "deepl-translate"

# DeepL supports these language codes:
# EN, DE, FR, ES, IT, PT, NL, PL, RU, JA, ZH, BG, CS, DA, EL, ET, FI, HU, LT, LV, RO, SK, SL, SV
DEFAULT_TARGET_LANGUAGE = os.environ.get("DEEPL_TARGET_LANG", "EN")


def translate_text(text: str, target_lang: str = DEFAULT_TARGET_LANGUAGE) -> str:
    """
    Translate a text string using the DeepL Translation API.
    Uses DeepL's neural machine translation engine.
    """
    if not text.strip():
        return ""

    response = requests.post(
        DEEPL_API_URL,
        data={
            "auth_key": DEEPL_API_KEY,
            "text": text,
            "target_lang": target_lang.upper(),
        },
        timeout=15,
    )
    response.raise_for_status()
    result = response.json()

    translations = result.get("translations", [])
    if translations:
        return translations[0].get("text", text)
    return text


def translate_record(
    record: DocumentRecord,
    target_lang: str = DEFAULT_TARGET_LANGUAGE,
) -> Dict[str, str]:
    """
    Translate all user-facing fields in a document record using DeepL API.
    Returns a mapping of field name to translated text.
    """
    user_fields = extract_user_facing_fields(record)
    translated: Dict[str, str] = {}

    for field_name, text in user_fields.items():
        translated[field_name] = translate_text(text, target_lang)

    return translated


def translate_records(
    records: List[DocumentRecord],
    target_lang: str = DEFAULT_TARGET_LANGUAGE,
) -> Dict[str, Dict[str, str]]:
    """
    Translate user-facing fields across multiple document records.
    Returns a mapping of doc_id to field-name-to-translation dict.
    """
    results: Dict[str, Dict[str, str]] = {}
    for record in records:
        results[record.doc_id] = translate_record(record, target_lang)
    return results
