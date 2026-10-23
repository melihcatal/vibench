from __future__ import annotations

"""Invoice note translation using DeepL API."""

import os

import deepl

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY", "")
DEEPL_TARGET_LANG = os.getenv("DEEPL_TARGET_LANG", "EN")


def invoice_note_translate(text: str, target_lang: str = DEEPL_TARGET_LANG) -> str:
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang=target_lang)
    return str(result)
