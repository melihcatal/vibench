import deepl
import os
from typing import Optional


def log_message_translate(message: str, target_lang: str = "es") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(message, target_lang=target_lang)
    return result.text
