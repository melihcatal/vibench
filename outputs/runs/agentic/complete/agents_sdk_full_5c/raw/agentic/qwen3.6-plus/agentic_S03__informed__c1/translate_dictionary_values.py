"""
Translates dictionary values while preserving keys.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

from typing import Any, Dict, Optional

from translation_client import get_client
from translation_models import DictionaryTranslationResult, TranslationResponse, TranslationResult


def translate_dictionary_values(
    data: Dict[str, str],
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> DictionaryTranslationResult:
    """
    Translate all string values in a dictionary while preserving keys.

    Uses DeepL's batch translation API to efficiently translate all values
    in a single API call, then reassembles results into a dictionary.

    Args:
        data: Dictionary with string keys and string values to translate.
        target_lang: Target language code (e.g., 'EN', 'DE', 'FR').
        source_lang: Source language code (optional).
        formality: Formality level ('prefer_more' or 'prefer_less'; optional).

    Returns:
        DictionaryTranslationResult containing original data, translated data,
        and the full TranslationResponse.
    """
    if not data:
        return DictionaryTranslationResult(
            original={},
            translated={},
            translations=TranslationResponse(),
        )

    client = get_client()

    # Preserve key order and extract values for batch translation
    keys = list(data.keys())
    values = list(data.values())

    # Batch translate all values at once
    batch_response = client.translate_batch(
        texts=values,
        target_lang=target_lang,
        source_lang=source_lang,
        formality=formality,
    )

    # Reconstruct dictionary with translated values
    translated: Dict[str, str] = {}
    for key, result in zip(keys, batch_response.results):
        translated[key] = result.text

    return DictionaryTranslationResult(
        original=data,
        translated=translated,
        translations=batch_response,
    )


def translate_nested_dictionary_values(
    data: Dict[str, Any],
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Recursively translate string values in a nested dictionary structure.

    Non-string values (int, float, bool, None) and sub-dictionaries are handled
    appropriately. Sub-dictionaries are recursively processed.

    Args:
        data: Nested dictionary with potentially string values to translate.
        target_lang: Target language code.
        source_lang: Source language code (optional).
        formality: Formality level (optional).

    Returns:
        New dictionary with all string values translated, keys and structure preserved.
    """
    # Collect all leaf string values for batch translation
    string_values: list[tuple[tuple, str]] = []
    _collect_strings(data, [], string_values)

    if not string_values:
        return data

    # Batch translate
    client = get_client()
    texts = [sv[1] for sv in string_values]
    batch_response = client.translate_batch(
        texts=texts,
        target_lang=target_lang,
        source_lang=source_lang,
        formality=formality,
    )

    # Reconstruct with translated values
    result_data = _copy_structure(data)
    for (path, _), translation in zip(string_values, batch_response.results):
        _set_value_at_path(result_data, path, translation.text)

    return result_data


def _collect_strings(
    data: Any, path: list, accumulator: list[tuple[tuple, str]]
) -> None:
    """Recursively collect all leaf string values with their key paths."""
    if isinstance(data, dict):
        for key, value in data.items():
            _collect_strings(value, path + [key], accumulator)
    elif isinstance(data, str):
        accumulator.append((tuple(path), data))


def _copy_structure(data: Any) -> Any:
    """Deep copy dictionary structure without string values."""
    if isinstance(data, dict):
        return {k: _copy_structure(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_copy_structure(item) for item in data]
    return data


def _set_value_at_path(data: Any, path: tuple, value: str) -> None:
    """Set a value at a specific key path in a nested dictionary."""
    obj = data
    for key in path[:-1]:
        obj = obj[key]
    obj[path[-1]] = value


if __name__ == "__main__":
    sample = {
        "greeting": "Hello",
        "farewell": "Goodbye",
        "message": "Welcome to our application",
    }
    result = translate_dictionary_values(sample, target_lang="DE")
    for key, value in result.translated.items():
        print(f"{key}: {value}")
