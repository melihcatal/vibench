from __future__ import annotations

import os

from deepl import Translator

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY", "")


_translator = Translator(DEEPL_AUTH_KEY) if DEEPL_AUTH_KEY else None


def translate_consent_text(text: str, target_lang: str = "EN-US") -> str:
    if _translator is None:
        return text
    result = _translator.translate_text(text, target_lang=target_lang)
    return str(result)
