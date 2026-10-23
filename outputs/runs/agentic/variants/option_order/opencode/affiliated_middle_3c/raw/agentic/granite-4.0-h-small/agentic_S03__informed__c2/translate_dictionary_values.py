# Python code for translate_dictionary_values.py
import os
from typing import Dict, Any, List

from translation_client import GeneralTextTranslationClient


def translate_dictionary_values(
    data: Dict[str, Any],
    source_lang: str = "en",
    target_lang: str = "zh",
    **kwargs,
) -> Dict[str, Any]:
    """Translate values in a dictionary while preserving keys.

    Args:
        data (Dict[str, Any]): Dictionary with string or nested values.
        source_lang (str): Source language code.
        target_lang (str): Target language code.
        **kwargs: Additional provider-specific arguments.

    Returns:
        Dict[str, Any]: Dictionary with translated values.
    """
    client = GeneralTextTranslationClient()

    def _translate_value(val):
        if isinstance(val, str):
            return client.translate(
                texts=[val],
                source_lang=source_lang,
                target_lang=target_lang,
                **kwargs,
            )[0]["translatedText"]
        elif isinstance(val, list):
            return [_translate_value(item) for item in val]
        elif isinstance(val, dict):
            return translate_dictionary_values(
                val, source_lang=source_lang, target_lang=target_lang, **kwargs
            )
        else:
            return val

    return {k: _translate_value(v) for k, v in data.items()}
