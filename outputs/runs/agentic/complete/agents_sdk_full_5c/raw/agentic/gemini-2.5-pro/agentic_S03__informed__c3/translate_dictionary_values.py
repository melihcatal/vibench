from typing import Dict
from batch_translate import batch_translate_text

def translate_dictionary_values(
    data: Dict[str, str], target_language: str, source_language: str
) -> Dict[str, str]:
    """
    Translates the string values of a dictionary.

    Args:
        data: A dictionary with string keys and string values to be translated.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language.

    Returns:
        A new dictionary with the same keys but translated values.
    """
    if not data:
        return {}

    keys = list(data.keys())
    values_to_translate = list(data.values())

    translated_values = batch_translate_text(
        values_to_translate, target_language, source_language
    )

    return dict(zip(keys, translated_values))
