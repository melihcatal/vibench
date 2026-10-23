"""
Translate appeal text for review using DeepL API.
"""
import os
from typing import Dict

import deepl


translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))


def translate_appeal(text: str, target_lang: str = "EN-US") -> Dict:
    """Translate appeal text for review."""
    result = translator.translate_text(text, target_lang=target_lang)
    return {
        "original_text": text,
        "translated_text": result.text,
        "detected_source_lang": result.detected_source_lang,
        "provider": "deepl"
    }