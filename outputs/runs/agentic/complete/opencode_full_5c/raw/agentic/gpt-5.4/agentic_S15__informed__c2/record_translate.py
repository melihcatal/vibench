from __future__ import annotations

import os
from typing import Any

import deepl

from database_models import filter_user_text_fields


def translate_record_fields(
    record: dict[str, Any], target_language: str, source_language: str | None = None
) -> dict[str, str]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    text_fields = filter_user_text_fields(record)
    translated: dict[str, str] = {}
    for field_name, text in text_fields.items():
        result = translator.translate_text(
            text, target_lang=target_language, source_lang=source_language
        )
        translated[field_name] = result.text
    return translated
