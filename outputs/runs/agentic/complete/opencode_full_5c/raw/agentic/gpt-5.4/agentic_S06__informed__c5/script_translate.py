from __future__ import annotations

import os

import deepl


def translate_script(
    text: str, target_language: str, source_language: str | None = None
) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text,
        target_lang=target_language,
        source_lang=source_language,
        model_type="prefer_quality_optimized",
    )
    return result.text
