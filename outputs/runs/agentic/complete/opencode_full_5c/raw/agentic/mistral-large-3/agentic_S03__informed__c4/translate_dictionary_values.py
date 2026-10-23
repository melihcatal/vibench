from google.cloud import translate_v2 as translate
from typing import Dict, Any
import os

# Provider: Google Cloud Translation (v2)
# Model: google/cloud-translate-v2


def translate_dictionary_values(
    data: Dict[str, Any], target_language: str, source_language: str = None
) -> Dict[str, Any]:
    """
    Translates dictionary values while preserving keys using Google Cloud Translation.

    Args:
        data: The dictionary to translate. Values must be strings.
        target_language: The target language code (e.g., 'es', 'fr').
        source_language: The source language code (optional, e.g., 'en').

    Returns:
        A new dictionary with translated values and original keys.
    """
    if not data:
        return data

    client = translate.Client()
    values = [str(v) for v in data.values() if isinstance(v, str)]

    if not values:
        return data

    results = client.translate(
        values, target_language=target_language, source_language=source_language
    )

    translated_values = [result["translatedText"] for result in results]
    translated_data = {}
    value_index = 0

    for key, value in data.items():
        if isinstance(value, str):
            translated_data[key] = translated_values[value_index]
            value_index += 1
        else:
            translated_data[key] = value

    return translated_data
