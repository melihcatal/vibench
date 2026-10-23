import os
from deepl import Translator

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


def translate_result(text: str, target_lang: str = "EN-US") -> str:
    translator = Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang=target_lang)
    return str(result)
