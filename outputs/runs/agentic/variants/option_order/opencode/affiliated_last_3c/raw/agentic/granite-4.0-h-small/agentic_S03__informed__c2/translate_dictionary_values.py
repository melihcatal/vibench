from typing import Dict, Any
from translation_client import TranslationClient


def translate_dictionary_values(
    data: Dict[str, Any], source_lang: str = "EN", target_lang: str = "FR"
) -> Dict[str, Any]:
    """Translate values in a dictionary while preserving keys.

    Args:
        data: Input dictionary with string values to translate.
        source_lang: Source language code.
        target_lang: Target language code.

    Returns:
        Dictionary with translated values.
    """
    client = TranslationClient()
    translated_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated_data[key] = client.translate(
                value, source_lang, target_lang
            ).translated_text
        else:
            translated_data[key] = value  # non-string values left unchanged
    return translated_data
