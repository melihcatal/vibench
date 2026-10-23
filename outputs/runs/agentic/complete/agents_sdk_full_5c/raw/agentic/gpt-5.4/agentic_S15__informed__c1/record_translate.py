from __future__ import annotations

import os
from typing import Dict, Iterable

import deepl


DEEPL_MODEL_TYPE = "prefer_quality_optimized"


def translate_fields(text_fields: Iterable[str], target_language: str, source_language: str | None = None) -> Dict[str, str]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    results: Dict[str, str] = {}
    for text in text_fields:
        if not text:
            continue
        translated = translator.translate_text(
            text,
            source_lang=source_language,
            target_lang=target_language,
            model_type=DEEPL_MODEL_TYPE,
        )
        results[text] = translated.text
    return results
