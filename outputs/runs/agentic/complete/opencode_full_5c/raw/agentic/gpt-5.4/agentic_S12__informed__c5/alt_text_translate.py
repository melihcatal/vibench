from __future__ import annotations

import os

import deepl


def alt_text_translate(text: str, target_language: str) -> dict:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_language)
    return {
        "translated_text": result.text,
        "target_language": target_language,
        "provider": "DeepL",
    }
