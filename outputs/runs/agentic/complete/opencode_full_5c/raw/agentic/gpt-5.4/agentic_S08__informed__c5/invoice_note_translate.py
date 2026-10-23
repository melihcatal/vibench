from __future__ import annotations

import os

import deepl


def translate_invoice_note(text: str, target_language: str = "EN-US") -> str:
    client = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = client.translate_text(text, target_lang=target_language)
    return result.text
