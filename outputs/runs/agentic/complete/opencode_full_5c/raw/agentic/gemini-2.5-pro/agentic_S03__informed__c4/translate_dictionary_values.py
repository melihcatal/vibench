from typing import Dict
from translation_client import get_translation_client


def translate_dictionary_values(
    data: Dict[str, str], target_language: str, source_language: str | None = None
) -> Dict[str, str]:
    """
    Translates the values of a dictionary.
    """
    client = get_translation_client()

    keys = list(data.keys())
    values = list(data.values())

    if not values:
        return {}

    translated_results = client.translate(
        values,
        target_language=target_language,
        source_language=source_language if source_language else "",
    )

    translated_dict = {}
    for i, key in enumerate(keys):
        translated_dict[key] = translated_results[i]["translatedText"]

    return translated_dict
