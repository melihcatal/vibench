import os
from translation_client import get_translation_client


def translate_dictionary_values(
    data: dict, source_lang: str = "en", target_lang: str = "es"
) -> dict:
    """Translate dictionary values while preserving keys.

    Uses Amazon Translate as the concrete provider.
    """
    translated = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated[key] = translate_text(value, source_lang, target_lang)
        elif isinstance(value, list):
            translated[key] = batch_translate(value, source_lang, target_lang)
        elif isinstance(value, dict):
            translated[key] = translate_dictionary_values(
                value, source_lang, target_lang
            )
        else:
            translated[key] = value
    return translated
