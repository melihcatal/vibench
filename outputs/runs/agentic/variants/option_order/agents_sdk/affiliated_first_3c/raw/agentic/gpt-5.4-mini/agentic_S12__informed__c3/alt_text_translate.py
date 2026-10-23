from __future__ import annotations

import os

from deepl import Translator

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY", "")


def translate_alt_text(text: str, target_lang: str = "EN-US"):
    translator = Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
