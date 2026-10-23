from __future__ import annotations

import os

from deep_translator import GoogleTranslator


def translate_consent_copy(text: str, target_language: str) -> str:
    translator = GoogleTranslator(source="auto", target=target_language)
    return translator.translate(text)
