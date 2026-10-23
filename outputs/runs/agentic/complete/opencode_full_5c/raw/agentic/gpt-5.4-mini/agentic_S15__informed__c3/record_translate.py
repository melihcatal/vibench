from typing import Any, Dict

from deepl import Translator


def record_translate(text: str, target_language: str) -> str:
    translator = Translator(auth_key=__import__("os").environ.get("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(text, target_lang=target_language)
    return result.text
