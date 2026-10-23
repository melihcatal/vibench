from __future__ import annotations

import os
from typing import Iterable, List

import deepl


def translate_ocr_text(
    text: str, target_language: str, source_language: str | None = None
) -> dict:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        target_lang=target_language.upper(),
        source_lang=source_language.upper() if source_language else None,
    )
    return {
        "provider": "deepl",
        "target_language": target_language.upper(),
        "translated_text": result.text,
        "detected_source_language": getattr(
            result, "detected_source_lang", source_language
        ),
    }


def translate_ocr_lines(
    lines: Iterable[str], target_language: str, source_language: str | None = None
) -> dict:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    source = source_language.upper() if source_language else None
    batch: List[str] = list(lines)
    results = translator.translate_text(
        batch, target_lang=target_language.upper(), source_lang=source
    )
    translated = [item.text for item in results]
    return {
        "provider": "deepl",
        "target_language": target_language.upper(),
        "translated_lines": translated,
    }
