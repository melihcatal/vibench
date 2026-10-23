# translate_text.py
import os
from typing import List
from translation_client import TranslationClient
from translation_models import validate_request, normalize_response

# Using DeepL as the concrete external provider
DEEPL_TARGET_LANG = "EN"

VALIDATE_REQUEST = validate_request
NORMALIZE_RESPONSE = normalize_response


def translate_text(source_text: str, target_lang: str = DEEPL_TARGET_LANG) -> str:
    """Translate a single string using DeepL."""
    validate_request(source_text, target_lang)
    raw = TranslationClient.translate_text(source_text, target_lang)
    return NORMALIZE_RESPONSE({"text": raw}).get("translated_text", source_text)


if __name__ == "__main__":
    example = "Hello, world!"
    print(f"Original: {example}")
    print(f"Translated: {translate_text(example)}")
