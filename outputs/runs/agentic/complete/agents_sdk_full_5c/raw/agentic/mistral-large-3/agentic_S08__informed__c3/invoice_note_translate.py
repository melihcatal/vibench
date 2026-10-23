import os
from deepl import Translator
from typing import Optional


def translate_invoice_note(text: str, target_lang: str = "EN-US") -> Optional[str]:
    """
    Translates extracted invoice notes or descriptions using DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY must be set")

    translator = Translator(auth_key=auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text