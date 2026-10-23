from __future__ import annotations

import os
from typing import Any

import deepl

from database_models import coerce_text_fields


def translate_record_fields(
    record: dict[str, Any],
    field_names: list[str],
    target_language: str,
    source_language: str | None = None,
) -> dict[str, Any]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    text_fields = coerce_text_fields(record, field_names)
    translated: dict[str, Any] = {}
    for field_name, text in text_fields.items():
        result = translator.translate_text(
            text, target_lang=target_language, source_lang=source_language
        )
        translated[field_name] = {
            "text": result.text,
            "detected_source_language": result.detected_source_lang,
        }
    return {
        "provider": "deepl",
        "target_language": target_language,
        "translations": translated,
    }
