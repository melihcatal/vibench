import os
import deepl
from typing import Optional


def welcome_translate(text: str, target_locale: str) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY not set")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_locale)
    return result.text
