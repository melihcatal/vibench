from __future__ import annotations

import os
from typing import Dict
from typing import Iterable

import deepl

from database_models import collect_text_fields


def translate_record_fields(
    document: Dict[str, object],
    fields: Iterable[str],
    target_language: str,
    source_language: str | None = None,
) -> Dict[str, str]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    text_fields = collect_text_fields(document, fields)
    translated: Dict[str, str] = {}
    for field_name, field_value in text_fields.items():
        result = translator.translate_text(
            field_value, target_lang=target_language, source_lang=source_language
        )
        translated[field_name] = result.text
    return translated
