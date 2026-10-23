from __future__ import annotations

from deepl import Translator


def alt_text_translate(text: str, target_language: str) -> str:
    translator = Translator(auth_key=None)
    result = translator.translate_text(text, target_lang=target_language.upper())
    return str(result)
