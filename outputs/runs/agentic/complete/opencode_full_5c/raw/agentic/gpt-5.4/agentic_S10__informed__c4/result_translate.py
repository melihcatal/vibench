from __future__ import annotations

import os

import deepl


def translate_result(
    text: str, target_language: str, source_language: str | None = None
) -> str:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(
        text,
        target_lang=target_language.upper(),
        source_lang=source_language.upper() if source_language else None,
    )
    return result.text
