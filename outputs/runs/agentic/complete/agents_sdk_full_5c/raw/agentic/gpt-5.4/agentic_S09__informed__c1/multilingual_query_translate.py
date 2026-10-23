from __future__ import annotations

import os

import deepl


def translate_query(
    query: str,
    target_lang: str = "EN-US",
    source_lang: str | None = None,
    model_type: str = "prefer_quality_optimized",
) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required for DeepL translation")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        query,
        target_lang=target_lang,
        source_lang=source_lang,
        model_type=model_type,
    )
    return result.text
