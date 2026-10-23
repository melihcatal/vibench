from __future__ import annotations

from deepl import Translator

TARGET_LANGUAGE = "EN-US"


def translate_appeal(text: str) -> str:
    translator = Translator(auth_key=None)
    result = translator.translate_text(text, target_lang=TARGET_LANGUAGE)
    return str(result)
