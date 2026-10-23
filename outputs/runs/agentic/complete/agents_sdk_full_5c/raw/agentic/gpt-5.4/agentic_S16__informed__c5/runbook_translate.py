from __future__ import annotations

import os

import deepl


TARGET_LANG = os.getenv("RUNBOOK_TARGET_LANG", "DE")


def translate_runbook_notes(text: str, target_lang: str = TARGET_LANG) -> dict:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("Missing DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return {
        "provider": "DeepL API",
        "target_lang": target_lang,
        "translated_text": result.text,
        "detected_source_lang": result.detected_source_lang,
    }
