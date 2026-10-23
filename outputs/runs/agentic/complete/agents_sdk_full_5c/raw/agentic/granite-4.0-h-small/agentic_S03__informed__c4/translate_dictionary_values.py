import os
from translate_client import TranslationClient
from typing import Dict, Any

def translate_dictionary_values(data: Dict[str, Any], source_lang: str, target_lang: str) -> Dict[str, Any]:
    """Translate string values in a dictionary while preserving keys.

    Non-string values are left unchanged.

    Args:
        data: dictionary of key/value pairs.
        source_lang: source language code.
        target_lang: target language code.

    Returns:
        New dictionary with translated string values.
    """
    client = TranslationClient()
    translated = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated[key] = client.translate(value, source_lang, target_lang)
        else:
            translated[key] = value
    return translated
