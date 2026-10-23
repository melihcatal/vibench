from __future__ import annotations

import os

import deepl


def translate_result(
    text: str, target_language: str, source_language: str | None = None
) -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text,
        target_lang=target_language,
        source_lang=source_language,
        preserve_formatting=True,
    )
    return result.text
