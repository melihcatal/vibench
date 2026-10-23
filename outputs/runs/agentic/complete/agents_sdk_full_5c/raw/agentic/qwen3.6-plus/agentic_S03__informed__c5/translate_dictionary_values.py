"""
translate_dictionary_values.py - Translates dictionary values while preserving keys using DeepL API.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY environment variable
"""

from typing import Any, Dict, List, Optional

from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse
from translation_client import TranslationClient


def translate_dictionary_values(
    data: Dict[str, Any],
    target_lang: str = "en",
    source_lang: Optional[str] = None,
    keys_to_skip: Optional[List[str]] = None,
) -> DictionaryTranslationResponse:
    """
    Translate all string values in a dictionary from source_lang to target_lang
    using the DeepL API, while preserving all keys.

    Non-string values (numbers, booleans, lists, nested dicts) are passed through
    unchanged. Keys listed in keys_to_skip are not translated.

    Args:
        data: Dictionary whose string values should be translated.
        target_lang: Target language code (e.g., 'en', 'de', 'fr'). Defaults to 'en'.
        source_lang: Source language code. If None, DeepL auto-detects the source.
        keys_to_skip: List of dictionary keys whose values should not be translated.

    Returns:
        DictionaryTranslationResponse with the translated dictionary and metadata.

    Raises:
        ValueError: If data is empty or contains no translatable string values.
        deepl.DeepLException: If the DeepL API request fails.
    """
    if not data:
        raise ValueError("Input dictionary must not be empty.")

    keys_to_skip = keys_to_skip or []
    has_string_values = any(
        isinstance(v, str) for k, v in data.items() if k not in keys_to_skip
    )
    if not has_string_values:
        raise ValueError("Input dictionary must contain at least one string value to translate.")

    request = DictionaryTranslationRequest(
        data=data,
        source_lang=source_lang,
        target_lang=target_lang,
        keys_to_skip=keys_to_skip,
    )

    client = TranslationClient()

    response = client.translate_dict_values(
        data=request.data,
        source_lang=request.source_lang,
        target_lang=request.target_lang,
        keys_to_skip=request.keys_to_skip,
    )

    return response
