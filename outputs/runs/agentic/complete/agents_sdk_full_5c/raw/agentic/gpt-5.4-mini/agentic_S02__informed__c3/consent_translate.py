from __future__ import annotations

from deepl import Translator


def translate_consent_copy(text: str, target_lang: str = "DE") -> str:
    translator = Translator(auth_key="DEEPL_AUTH_KEY")
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
