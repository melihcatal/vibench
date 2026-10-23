"""Translate dictionary values while preserving keys using DeepL API."""

import os
from deepl import Translator

from translation_models import TranslationRequest, TranslationResponse


def translate_dictionary_values(
    input_dict: dict[str, str],
    target_lang: str,
    source_lang: str | None = None,
    skip_keys: set[str] | None = None,
) -> dict[str, str]:
    """Translate all values in a dictionary while preserving keys using DeepL.

    Args:
        input_dict: Dictionary with string values to translate.
        target_lang: Target language code (e.g., 'ES', 'FR', 'JA').
        source_lang: Source language code. If None, DeepL auto-detects.
        skip_keys: Optional set of keys whose values should not be translated.

    Returns:
        New dictionary with translated values and original keys preserved.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required for DeepL API access")

    translator = Translator(auth_key)

    kwargs: dict[str, str | None] = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang

    keys_to_translate = [
        k for k in input_dict if skip_keys is None or k not in skip_keys
    ]
    values_to_translate = [input_dict[k] for k in keys_to_translate]

    if not values_to_translate:
        return dict(input_dict)

    results = translator.translate_text(values_to_translate, **kwargs)

    output: dict[str, str] = dict(input_dict)
    for key, result in zip(keys_to_translate, results):
        output[key] = result.text

    return output
