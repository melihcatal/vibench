import os
from deepl import Translator


def translate_invoice_note(text: str, target_lang: str = "en-US") -> str:
    """
    Translate invoice notes using DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY required.")

    translator = Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
