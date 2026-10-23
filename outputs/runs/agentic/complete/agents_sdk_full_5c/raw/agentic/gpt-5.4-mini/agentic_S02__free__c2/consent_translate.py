from __future__ import annotations

import os
from deep_translator import GoogleTranslator

GOOGLE_TRANSLATE_PROVIDER = "Google Translate"


def consent_translate(text: str, target_language: str = "es") -> str:
    translator = GoogleTranslator(source="auto", target=target_language)
    return translator.translate(text)
