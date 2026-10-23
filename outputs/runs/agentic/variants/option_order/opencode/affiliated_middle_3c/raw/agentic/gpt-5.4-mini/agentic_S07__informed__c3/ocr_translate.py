import os

from deepl import Translator


def translate_ocr_text(text: str, target_language: str = "EN-US") -> str:
    key = os.environ.get("DEEPL_AUTH_KEY", "").strip()
    if not key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = Translator(key)
    return translator.translate_text(text, target_lang=target_language).text
