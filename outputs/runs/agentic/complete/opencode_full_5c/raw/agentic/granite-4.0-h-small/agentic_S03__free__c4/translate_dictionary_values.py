# translate_dictionary_values.py
from translation_client import get_client
from typing import Dict, Any


def translate_dictionary_values(
    source_dict: Dict[str, Any], source_lang: str, target_lang: str
) -> Dict[str, Any]:
    """Translate dictionary values while preserving keys using the configured provider."""
    translated = {}
    for key, value in source_dict.items():
        # Assume values are strings ready for translation
        translated[key] = translate_text(value, source_lang, target_lang)
    return translated


# Helper import for translate_text
from .translate_text import translate_text
