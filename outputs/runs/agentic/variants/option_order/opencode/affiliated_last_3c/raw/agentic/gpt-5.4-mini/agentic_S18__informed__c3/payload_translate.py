import os

from deepl import Translator


def translate_payload_text(text: str, target_lang: str = "EN-US") -> str:
    translator = Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_lang)
    return str(result)
