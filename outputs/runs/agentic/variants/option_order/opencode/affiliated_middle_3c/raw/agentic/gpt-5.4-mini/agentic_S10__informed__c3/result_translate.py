import os
from deepl import Translator


def translate_result(text: str, target_lang: str = "EN-US") -> str:
    translator = Translator(os.getenv("DEEPL_AUTH_KEY", ""))
    return translator.translate_text(text, target_lang=target_lang).text
