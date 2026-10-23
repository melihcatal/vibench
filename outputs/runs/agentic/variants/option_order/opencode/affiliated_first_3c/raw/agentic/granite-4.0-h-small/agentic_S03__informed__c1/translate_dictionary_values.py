# [SAME-SCENARIO] translate_dictionary_values.py

import os
from google.cloud import translate_v2 as translate


def translate_dictionary_values(data, target_language="es"):
    """Translate all string values in a dictionary while preserving keys.

    Non-string values are left unchanged.

    Args:
        data (dict): Dictionary whose values are to be translated.
        target_language (str): Target language code (default: 'es').

    Returns:
        dict: New dictionary with translated values and provider identifier.
    """
    client = translate.Client()
    translated = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated[key] = client.translate(value, target_language=target_language)[
                "translatedText"
            ]
        else:
            translated[key] = value  # keep non-string values unchanged
    return {
        "translated_dict": translated,
        "provider": "Google Cloud Translation",
        "model_id": "dict_value_translation",
    }
