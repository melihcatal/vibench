import os
from typing import Dict, Optional
from google.cloud import translate_v2 as translate


def translate_dictionary_values(
    dictionary: Dict[str, str],
    target_language: str,
    source_language: Optional[str] = None,
) -> Dict[str, str]:
    """
    Translate dictionary values while preserving keys using Google Cloud Translation API.

    Args:
        dictionary: Dictionary with string values to translate
        target_language: Target language code (e.g., 'es', 'fr', 'de')
        source_language: Optional source language code (e.g., 'en')

    Returns:
        Dictionary with same keys and translated values
    """
    client = translate.Client()

    # Extract values for batch translation
    keys = list(dictionary.keys())
    values = list(dictionary.values())

    if source_language:
        results = client.translate(
            values, target_language=target_language, source_language=source_language
        )
    else:
        results = client.translate(values, target_language=target_language)

    # Reconstruct dictionary with translated values
    translated_dict = {}
    for key, result in zip(keys, results):
        translated_dict[key] = result["translatedText"]

    return translated_dict
