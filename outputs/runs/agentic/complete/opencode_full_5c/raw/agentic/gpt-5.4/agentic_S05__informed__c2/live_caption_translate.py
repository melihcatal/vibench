from __future__ import annotations

import os

import deepl


def translate_live_caption(
    text: str, target_language: str, source_language: str | None = None
) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text, target_lang=target_language, source_lang=source_language
    )
    return result.text
