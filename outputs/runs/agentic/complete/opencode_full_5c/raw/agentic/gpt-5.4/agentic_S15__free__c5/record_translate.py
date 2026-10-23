from __future__ import annotations

import os

import deepl

from database_models import extract_user_text_fields


def record_translate(
    document: dict[str, object], target_language: str
) -> dict[str, str]:
    fields = extract_user_text_fields(document)
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    translated: dict[str, str] = {}
    for key, value in fields.items():
        result = translator.translate_text(value, target_lang=target_language)
        translated[key] = result.text
    return translated
