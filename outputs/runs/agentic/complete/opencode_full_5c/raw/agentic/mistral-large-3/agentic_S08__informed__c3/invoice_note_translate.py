import os
from typing import Dict, Any
from deepl import Translator


def translate_invoice_notes(text: str, target_lang: str = "EN-US") -> str:
    """
    Translates extracted invoice notes or descriptions using DeepL API.
    """
    translator = Translator(auth_key=os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
