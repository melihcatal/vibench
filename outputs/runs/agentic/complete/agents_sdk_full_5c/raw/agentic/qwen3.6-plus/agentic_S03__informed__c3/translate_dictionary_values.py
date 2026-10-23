"""Translate dictionary values while preserving keys.

Provider: DeepL API (deepl SDK)
Auth: DEEPL_AUTH_KEY
"""

from __future__ import annotations

from translation_client import get_client
from translation_models import (
    BatchTranslationResponse,
    TranslationResponse,
    deepl_result_to_response,
    normalize_language_code,
    normalize_formality,
)


def translate_dictionary_values(
    source_dict: dict[str, str],
    source_lang: str = "",
    target_lang: str = "EN",
    formality: str = "default",
) -> dict[str, str]:
    """Translate all string values in a dictionary, preserving keys.

    Uses DeepL batch translation internally for efficiency.

    Args:
        source_dict: Dictionary with string values to translate.
        source_lang: Source language code. Auto-detected if empty.
        target_lang: Target language code. Defaults to 'EN'.
        formality: Formality level for the translation.

    Returns:
        New dictionary with the same keys and translated values.
    """
    if not source_dict:
        return {}

    normalized_source = normalize_language_code(source_lang)
    normalized_target = normalize_language_code(target_lang)
    norm_formality = normalize_formality(formality)

    # Preserve insertion order
    keys = list(source_dict.keys())
    values = [source_dict[k] for k in keys]

    client = get_client()
    deepl_results = client.translate_list(
        texts=values,
        source_lang=normalized_source,
        target_lang=normalized_target,
        formality=norm_formality,
    )

    translated: dict[str, str] = {}
    for key, result in zip(keys, deepl_results):
        translated[key] = result.text

    return translated


def translate_nested_dictionary_values(
    source_dict: dict[str, object],
    source_lang: str = "",
    target_lang: str = "EN",
    formality: str = "default",
) -> dict[str, object]:
    """Recursively translate string values in a nested dictionary.

    Only leaf string values are translated; nested dicts and lists are traversed.

    Args:
        source_dict: Nested dictionary structure.
        source_lang: Source language code.
        target_lang: Target language code.
        formality: Formality level.

    Returns:
        New dictionary with translated string leaves.
    """
    result: dict[str, object] = {}
    for key, value in source_dict.items():
        if isinstance(value, dict):
            result[key] = translate_nested_dictionary_values(
                value, source_lang, target_lang, formality
            )
        elif isinstance(value, str):
            translated = translate_dictionary_values(
                {key: value}, source_lang, target_lang, formality
            )
            result[key] = translated.get(key, value)
        elif isinstance(value, list):
            result[key] = [
                translate_nested_dictionary_values(
                    {str(idx): item}, source_lang, target_lang, formality
                ).get(str(idx), item)
                if isinstance(item, (dict, str))
                else item
                for idx, item in enumerate(value)
            ]
        else:
            result[key] = value
    return result
