from __future__ import annotations

import os
from typing import Any

import deepl


def translate_record_fields(
    text_fields: dict[str, Any],
    target_language: str,
    source_language: str | None = None,
) -> dict[str, Any]:
    translator = deepl.Translator(os.environ.get("DEEPL_AUTH_KEY"))
    translated: dict[str, str] = {}
    for key, value in text_fields.items():
        if value is None:
            continue
        result = translator.translate_text(
            str(value),
            target_lang=target_language,
            source_lang=source_language,
        )
        translated[key] = result.text
    return {
        "provider": "deepl",
        "target_language": target_language,
        "translations": translated,
    }
