import os
from deepl import Translator
from typing import Optional


def localize_platform_output(text: str, target_lang: str = "ES") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    translator = Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
