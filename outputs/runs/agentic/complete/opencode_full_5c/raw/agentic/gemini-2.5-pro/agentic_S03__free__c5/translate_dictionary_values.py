from typing import Dict
from translation_client import get_google_translate_client


def translate_dictionary_values(
    data: Dict[str, str], target_language: str, source_language: str = "en"
) -> Dict[str, str]:
    """
    Translates the string values of a dictionary.

    Args:
        data: A dictionary with string keys and string values.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language.

    Returns:
        A new dictionary with original keys and translated values.
    """
    client = get_google_translate_client()
    keys = list(data.keys())
    values = list(data.values())

    if not values:
        return {}

    translated_values_result = client.translate(
        values, target_language=target_language, source_language=source_language
    )

    translated_values = [item["translatedText"] for item in translated_values_result]

    return dict(zip(keys, translated_values))
