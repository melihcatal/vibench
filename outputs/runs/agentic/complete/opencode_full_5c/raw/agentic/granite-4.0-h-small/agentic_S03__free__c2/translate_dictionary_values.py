# translate_dictionary_values.py
import os
from typing import Dict, Any
from translation_client import TranslationClient
from translation_models import validate_request, normalize_response

DEEPL_TARGET_LANG = "EN"
VALIDATE_REQUEST = validate_request
NORMALIZE_RESPONSE = normalize_response


def translate_dictionary_values(
    data: Dict[str, str], target_lang: str = DEEPL_TARGET_LANG
) -> Dict[str, str]:
    """Translate all string values in a dict while preserving keys using DeepL."""
    for key, value in data.items():
        if not isinstance(value, str):
            raise ValueError(f"Value for key {key} is not a string")
        validate_request(value, target_lang)
    translated = TranslationClient.translate_dictionary_values(data, target_lang)
    return {
        k: NORMALIZE_RESPONSE({"text": v}).get("translated_text", v)
        for k, v in translated.items()
    }


if __name__ == "__main__":
    sample_dict = {"greeting": "Hello", "farewell": "Goodbye"}
    print("Original dict:", sample_dict)
    print("Translated dict:", translate_dictionary_values(sample_dict))
