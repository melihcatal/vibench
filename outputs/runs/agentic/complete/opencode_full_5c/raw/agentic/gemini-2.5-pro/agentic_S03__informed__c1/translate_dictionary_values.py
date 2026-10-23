from typing import Dict
from translation_client import get_translation_client


def translate_dictionary_values(
    data: Dict[str, str], target_language: str, source_language: str = "en"
) -> Dict[str, str]:
    """
    Translates the values of a dictionary.

    Args:
        data: A dictionary with string keys and string values to be translated.
        target_language: The target language code.
        source_language: The source language code.

    Returns:
        A new dictionary with the same keys and translated values.
    """
    client = get_translation_client()
    keys = list(data.keys())
    values = list(data.values())

    if not values:
        return {}

    translated_values_result = client.translate(
        values, target_language=target_language, source_language=source_language
    )

    translated_values = [item["translatedText"] for item in translated_values_result]

    return dict(zip(keys, translated_values))
