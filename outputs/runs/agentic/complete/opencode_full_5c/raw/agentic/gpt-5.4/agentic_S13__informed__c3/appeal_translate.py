from __future__ import annotations

import os

import deepl


def translate_appeal(
    text: str, target_lang: str = "EN-US", source_lang: str | None = None
) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise ValueError("Missing DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text, target_lang=target_lang, source_lang=source_lang
    )
    return result.text
