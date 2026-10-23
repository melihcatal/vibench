"""
translate_dictionary_values.py - Translates dictionary values while preserving keys
using Google Cloud Translation API v3.
"""

from typing import Dict, Optional, List
from google.cloud import translate_v3 as translate

from translation_client import get_translation_client, get_project_location, validate_client_ready
from translation_models import (
    TranslationResult,
    DictionaryTranslationResult,
    normalize_language_code,
    validate_translation_response,
)


def translate_dictionary_values(
    dictionary: Dict[str, str],
    source_language: str = "auto",
    target_language: str = "es",
    model: str = "nmt",
) -> DictionaryTranslationResult:
    """
    Translate dictionary values while preserving original keys using Google
    Cloud Translation API v3.

    Uses batch translation under the hood to efficiently translate all values
    in a single API call (up to 128 values per request, with chunking for
    larger dictionaries).

    Args:
        dictionary: Dictionary with string values to translate.
        source_language: Source language code (BCP-47).
        target_language: Target language code (BCP-47).
        model: Translation model ("nmt" for Google Neural Machine Translation).

    Returns:
        DictionaryTranslationResult with original and translated dictionaries.
    """
    if not validate_client_ready():
        raise RuntimeError(
            "Google Cloud Translation client not configured. "
            "Set GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS."
        )

    if not dictionary:
        return DictionaryTranslationResult(
            original={},
            translated={},
            target_language=target_language,
        )

    source_lang = normalize_language_code(source_language)
    target_lang = normalize_language_code(target_language)

    client = get_translation_client()
    parent = get_project_location()

    model_path = f"{parent}/models/{model}" if model != "nmt" else None

    ordered_keys = list(dictionary.keys())
    values_to_translate = [dictionary[k] for k in ordered_keys]

    translated_values: Dict[str, str] = {}
    google_batch_limit = 128

    for i in range(0, len(values_to_translate), google_batch_limit):
        chunk = values_to_translate[i : i + google_batch_limit]
        chunk_keys = ordered_keys[i : i + google_batch_limit]

        request = translate.TranslateTextRequest(
            contents=chunk,
            target_language_code=target_lang,
            parent=parent,
            model=model_path,
        )

        if source_lang != "auto":
            request.source_language_code = source_lang

        response = client.translate_text(request=request)

        for idx, translation in enumerate(response.translations):
            translated_text = validate_translation_response(
                translation.translated_text
            )
            if translated_text is None:
                translated_text = chunk[idx]
            key = chunk_keys[idx]
            translated_values[key] = translated_text

    return DictionaryTranslationResult(
        original=dictionary,
        translated=translated_values,
        target_language=target_lang,
    )


if __name__ == "__main__":
    sample_dict = {
        "greeting": "Hello",
        "farewell": "Goodbye",
        "thanks": "Thank you very much",
    }
    result = translate_dictionary_values(sample_dict, target_language="it")
    for key, val in result.translated.items():
        print(f"  {key}: {val}")
