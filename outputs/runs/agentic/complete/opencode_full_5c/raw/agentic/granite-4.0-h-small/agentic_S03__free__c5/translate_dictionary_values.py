import os
from typing import Dict, Any
from translation_client import TranslationClient
from translation_models import GeneralTextRequest, GeneralTextResponse


def translate_dictionary_values(
    data: Dict[str, Any], source_lang: str = "en", target_lang: str = "es"
) -> Dict[str, Any]:
    """Translate dictionary values while preserving keys.

    Args:
        data: Dictionary containing string or nested dict values to translate.
        source_lang: ISO language code for source (default "en").
        target_lang: ISO language code for target (default "es").

    Returns:
        New dictionary with translated values, retaining original keys and structure.
    """
    translated = {}
    for key, value in data.items():
        if isinstance(value, dict):
            # Recursively translate nested dictionaries
            translated[key] = translate_dictionary_values(
                value, source_lang, target_lang
            )
        elif isinstance(value, str):
            # Translate string values
            translated[key] = translate_text(value, source_lang, target_lang)
        else:
            # Non-string values are copied unchanged
            translated[key] = value
    return translated


# Helper imports from same-scenario file
from translate_text import translate_text
