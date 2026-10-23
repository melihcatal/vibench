import os

from deepl import Translator


def translate_payload(text: str, target_lang: str = "EN-US"):
    auth_key = os.getenv("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    translator = Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
