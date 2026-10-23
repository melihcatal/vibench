from __future__ import annotations

from deepL import DeeplTranslator


def alt_text_translate(text: str, target_language: str = "es") -> str:
    translator = DeeplTranslator(auth_key="DEEPL_AUTH_KEY")
    result = translator.translate_text(text, target_lang=target_language.upper())
    return str(result)
