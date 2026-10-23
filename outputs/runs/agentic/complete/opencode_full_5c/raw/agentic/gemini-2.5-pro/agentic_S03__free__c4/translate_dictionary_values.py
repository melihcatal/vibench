from typing import Dict
from translation_client import get_translation_client


def translate_dictionary(
    data: Dict[str, str], target_language: str, source_language: str = None
) -> Dict[str, str]:
    """
    Translates the values of a dictionary.

    Args:
        data: A dictionary with string values to translate.
        target_language: The language to translate the values into.
        source_language: The source language of the text.

    Returns:
        A new dictionary with the same keys and translated values.
    """
    client = get_translation_client()

    values_to_translate = list(data.values())

    if not values_to_translate:
        return {}

    translated_values_result = client.translate(
        values_to_translate,
        target_language=target_language,
        source_language=source_language if source_language else "",
    )

    translated_values = [item["translatedText"] for item in translated_values_result]

    return dict(zip(data.keys(), translated_values))
