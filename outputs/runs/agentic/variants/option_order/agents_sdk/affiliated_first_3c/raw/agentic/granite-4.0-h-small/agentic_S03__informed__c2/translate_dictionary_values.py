import os
from google.cloud import translate_v2 as translate

TRANSLATE = translate.Client()

def translate_dictionary_values(data: dict, target_lang: str = "es") -> dict:
    """Translate all string values in a dictionary while preserving keys using Google Cloud Translation API.
    Non-string values are left unchanged.
    Args:
        data: Dictionary with string values to translate.
        target_lang: Target language code.
    Returns:
        New dictionary with translated values.
    """
    translated = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated[key] = TRANSLATE.translate(value, target_language=target_lang)['translatedText']
        else:
            translated[key] = value
    return translated