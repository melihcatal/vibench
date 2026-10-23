import os
from typing import Dict, Any
import deepl


def translate_appeal(text: str, target_lang: str = "EN-US") -> str:
    """Translate appeal text for review using DeepL API."""
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DeepL auth key must be set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text