from typing import Dict
from translation_client import get_translation_client


def translate_dictionary_values(
    data: Dict[str, str], target_language: str, source_language: str = "en"
) -> Dict[str, str]:
    """
    Translates the values of a dictionary using Google Cloud Translation.
    """
    client = get_translation_client()

    if not data:
        return {}

    keys = list(data.keys())
    values = list(data.values())

    translated_values = client.translate(
        values, target_language=target_language, source_language=source_language
    )

    translated_dict = {}
    for i, key in enumerate(keys):
        translated_dict[key] = translated_values[i]["translatedText"]

    return translated_dict
