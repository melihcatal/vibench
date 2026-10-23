import os
import deepl
from typing import Dict, List

from translation_client import get_deepl_api_key

def translate_dictionary_values(
    data: Dict[str, str], target_language: str, source_language: str = "EN"
) -> Dict[str, str]:
    """
    Translates the string values of a dictionary using the DeepL API.

    Args:
        data: A dictionary with string keys and string values to be translated.
        target_language: The target language code (e.g., 'FR', 'ES').
        source_language: The source language code (e.g., 'EN', 'DE').

    Returns:
        A new dictionary with the same keys but with translated values.
    """
    auth_key = get_deepl_api_key()
    translator = deepl.Translator(auth_key)

    if not data:
        return {}

    keys = list(data.keys())
    values_to_translate = list(data.values())

    # DeepL target_lang parameter uses codes like "FR", "EN-US"
    # The SDK handles mapping for most common cases.
    result = translator.translate_text(
        values_to_translate,
        source_lang=source_language.upper(),
        target_lang=target_language.upper(),
    )

    translated_values: List[str] = [item.text for item in result]

    return dict(zip(keys, translated_values))
