from __future__ import annotations

import os

import deepl


DEFAULT_TARGET_LANG = "DE"


def translate_runbook(note: str, target_lang: str = DEFAULT_TARGET_LANG) -> dict:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(note, target_lang=target_lang)
    return {
        "provider": "deepl",
        "target_lang": target_lang,
        "detected_source_lang": result.detected_source_lang,
        "translated_text": result.text,
    }
