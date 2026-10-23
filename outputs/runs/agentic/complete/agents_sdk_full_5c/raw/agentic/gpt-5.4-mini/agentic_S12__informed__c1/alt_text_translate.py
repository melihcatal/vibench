from __future__ import annotations

from deepl import Translator

TARGET_LANG = "ES"


def translate_alt_text(text: str, target_lang: str = TARGET_LANG) -> str:
    translator = Translator(auth_key="")
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
