import os

from deepl import Translator


def translate_script(text: str, target_lang: str = "EN-US") -> str:
    key = os.getenv("DEEPL_AUTH_KEY")
    if not key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    translator = Translator(key)
    return translator.translate_text(text, target_lang=target_lang).text
