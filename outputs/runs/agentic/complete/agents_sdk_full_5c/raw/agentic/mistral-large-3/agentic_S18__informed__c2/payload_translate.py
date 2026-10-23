"""Translate customer-facing message payload text using DeepL."""
import os
from typing import Dict, Any
import deepl


translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))


def translate_payload(text: str, target_lang: str = "EN-US") -> str:
    """Translate text using DeepL API."""
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text