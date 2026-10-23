from __future__ import annotations

import os

import deepl


def translate_invoice_note(text: str, target_language: str = "EN-US") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("Missing required environment variable: DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_language)
    return result.text
