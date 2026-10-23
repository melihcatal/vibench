from __future__ import annotations

import os

import deepl


def translate_script(text: str, target_lang: str = "EN-US", source_lang: str | None = None) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    client = deepl.Translator(auth_key)
    result = client.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return result.text
