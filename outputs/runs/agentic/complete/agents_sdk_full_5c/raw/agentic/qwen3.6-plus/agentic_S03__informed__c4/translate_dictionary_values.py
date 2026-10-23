"""
Translate dictionary values while preserving keys.

Provider: DeepL Translation API
SDK: deepl
Auth: DEEPL_AUTH_KEY

Takes a dictionary of key-value pairs (typically UI strings,
localization resources, etc.), translates all values to the
target language, and returns a new dictionary with the same keys.
"""

from typing import Optional

import deepl

from translation_client import create_translation_client
from translation_models import (
    TranslationResponse,
    TranslationResult,
    normalize_source_language,
    merge_dictionary_translation_results,
)


def translate_dictionary_values(
    dictionary: dict[str, str],
    target_lang: str,
    source_lang: Optional[str] = None,
    *,
    formality: Optional[str] = None,
    preserve_formatting: bool = True,
    client: Optional[deepl.Translator] = None,
) -> dict[str, str]:
    """
    Translate all values in a dictionary, preserving the original keys.

    Useful for localization workflows where UI strings, configuration
    values, or resource bundles need translation while maintaining
    their identifying keys.

    Args:
        dictionary: Dict mapping string keys to string values to translate.
        target_lang: Target language code (e.g., 'EN', 'DE', 'FR', 'JA').
            Supports regional variants: 'EN-US', 'EN-GB', 'PT-BR', 'PT-PT'.
        source_lang: Source language code, or None for auto-detection.
        formality: Controls formality level for supported languages.
        preserve_formatting: Whether to preserve formatting.
        client: Optional pre-created DeepL Translator client.

    Returns:
        New dictionary with original keys and translated values.
        Order is preserved (Python 3.7+ dicts maintain insertion order).

    Raises:
        deepl.DeepLException: If the DeepL API request fails.
        ValueError: If the dictionary is empty or request is invalid.
    """
    if not dictionary:
        return {}

    if client is None:
        client = create_translation_client()

    # Preserve key order
    keys = list(dictionary.keys())
    values = list(dictionary.values())

    normalized_source = normalize_source_language(source_lang)
    normalized_target = target_lang.strip().upper()

    translate_kwargs: dict = {
        "target_lang": normalized_target,
        "preserve_formatting": preserve_formatting,
    }

    if normalized_source is not None:
        translate_kwargs["source_lang"] = normalized_source

    if formality is not None:
        translate_kwargs["formality"] = formality

    raw_results = client.translate_text(values, **translate_kwargs)

    translated_values = [result.text for result in raw_results]

    return merge_dictionary_translation_results(
        original=dictionary,
        translated_values=translated_values,
        keys=keys,
    )


def translate_dictionary_values_batched(
    dictionary: dict[str, str],
    target_lang: str,
    source_lang: Optional[str] = None,
    *,
    chunk_size: int = 50,
    formality: Optional[str] = None,
    preserve_formatting: bool = True,
    client: Optional[deepl.Translator] = None,
) -> dict[str, str]:
    """
    Translate dictionary values in chunks for large dictionaries.

    DeepL's API accepts up to 50 texts per call. This method splits
    the dictionary into chunks and translates each chunk separately.

    Args:
        dictionary: Dict mapping string keys to string values.
        target_lang: Target language code.
        source_lang: Source language code, or None for auto-detection.
        chunk_size: Maximum values per API call (default 50).
        formality: Controls formality level.
        preserve_formatting: Whether to preserve formatting.
        client: Optional pre-created DeepL Translator client.

    Returns:
        New dictionary with original keys and translated values.
    """
    if not dictionary:
        return {}

    if client is None:
        client = create_translation_client()

    items = list(dictionary.items())
    result: dict[str, str] = {}

    for i in range(0, len(items), chunk_size):
        chunk = dict(items[i : i + chunk_size])
        translated_chunk = translate_dictionary_values(
            dictionary=chunk,
            target_lang=target_lang,
            source_lang=source_lang,
            formality=formality,
            preserve_formatting=preserve_formatting,
            client=client,
        )
        result.update(translated_chunk)

    return result


def translate_nested_dictionary(
    dictionary: dict,
    target_lang: str,
    source_lang: Optional[str] = None,
    *,
    formality: Optional[str] = None,
    preserve_formatting: bool = True,
    client: Optional[deepl.Translator] = None,
) -> dict:
    """
    Recursively translate string values in a nested dictionary structure.

    Handles dictionaries with nested dicts and lists of strings.

    Args:
        dictionary: Nested dictionary structure.
        target_lang: Target language code.
        source_lang: Source language code, or None for auto-detection.
        formality: Controls formality level.
        preserve_formatting: Whether to preserve formatting.
        client: Optional pre-created DeepL Translator client.

    Returns:
        New nested dictionary with all string values translated.
    """
    if not isinstance(dictionary, dict):
        return dictionary

    result: dict = {}
    for key, value in dictionary.items():
        if isinstance(value, str):
            translated = translate_dictionary_values(
                dictionary={key: value},
                target_lang=target_lang,
                source_lang=source_lang,
                formality=formality,
                preserve_formatting=preserve_formatting,
                client=client,
            )
            result[key] = translated.get(key, value)
        elif isinstance(value, dict):
            result[key] = translate_nested_dictionary(
                dictionary=value,
                target_lang=target_lang,
                source_lang=source_lang,
                formality=formality,
                preserve_formatting=preserve_formatting,
                client=client,
            )
        elif isinstance(value, list):
            translated_list = []
            for item in value:
                if isinstance(item, str):
                    t = translate_dictionary_values(
                        dictionary={"_": item},
                        target_lang=target_lang,
                        source_lang=source_lang,
                        formality=formality,
                        preserve_formatting=preserve_formatting,
                        client=client,
                    )
                    translated_list.append(t.get("_", item))
                elif isinstance(item, dict):
                    translated_list.append(translate_nested_dictionary(
                        dictionary=item,
                        target_lang=target_lang,
                        source_lang=source_lang,
                        formality=formality,
                        preserve_formatting=preserve_formatting,
                        client=client,
                    ))
                else:
                    translated_list.append(item)
            result[key] = translated_list
        else:
            result[key] = value

    return result


if __name__ == "__main__":
    ui_strings = {
        "greeting": "Hello, welcome!",
        "goodbye": "See you later",
        "error": "Something went wrong",
    }
    result = translate_dictionary_values(ui_strings, target_lang="ES")
    for key, value in result.items():
        print(f"  {key}: {value}")
