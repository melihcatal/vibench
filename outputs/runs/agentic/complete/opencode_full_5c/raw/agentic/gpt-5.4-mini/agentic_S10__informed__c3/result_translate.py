import os
from deepl import Translator


def result_translate(text: str, target_lang: str = "EN-US") -> str:
    translator = Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
