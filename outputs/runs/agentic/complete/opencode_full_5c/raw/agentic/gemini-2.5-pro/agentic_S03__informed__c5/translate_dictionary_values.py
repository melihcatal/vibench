from typing import Dict
from translation_client import get_translation_client


def translate_dictionary_values(
    data: Dict[str, str], source_language: str, target_language: str
) -> Dict[str, str]:
    """
    Translates the string values of a dictionary using Google Cloud Translation.
    """
    client = get_translation_client()

    keys = list(data.keys())
    values_to_translate = list(data.values())

    if not values_to_translate:
        return {}

    translated_results = client.translate(
        values_to_translate,
        target_language=target_language,
        source_language=source_language,
    )

    translated_values = [result["translatedText"] for result in translated_results]

    return dict(zip(keys, translated_values))
