import os
from typing import Dict, Any
from translation_client import TranslationClient


def translate_dictionary_values(
    data_dict: Dict[str, Any], source_lang: str = "en", target_lang: str = "es"
) -> Dict[str, Any]:
    """
    Translate dictionary values while preserving keys using Google Cloud Translation API.

    Args:
        data_dict: Dictionary with string values to translate
        source_lang: Source language code (default: "en")
        target_lang: Target language code (default: "es")

    Returns:
        Dictionary with same keys but translated values
    """
    client = TranslationClient()

    # Use Google Cloud Translation API
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    result_dict = {}

    for key, value in data_dict.items():
        if isinstance(value, str) and value.strip():
            # Translate string values
            if isinstance(value, bytes):
                value = value.decode("utf-8")

            translation_result = translate_client.translate(
                value, source_language=source_lang, target_language=target_lang
            )

            result_dict[key] = translation_result["translatedText"]
        else:
            # Preserve non-string values as-is
            result_dict[key] = value

    return result_dict
