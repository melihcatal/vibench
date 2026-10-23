from typing import Optional

from deep_translator import GoogleTranslator


def translate_consent_copy(text: str, target_language: str, source_language: str = "auto") -> str:
    translator = GoogleTranslator(source=source_language, target=target_language)
    return translator.translate(text)
