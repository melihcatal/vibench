import os
from deepl import Translator

translator = Translator(os.getenv("DEEPL_API_KEY"))


def consent_translate(text: str, target_lang: str = "EN-US") -> str:
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
