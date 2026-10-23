import os
from deepl import Translator


def ocr_translate(text: str, target_lang: str = "ES") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
