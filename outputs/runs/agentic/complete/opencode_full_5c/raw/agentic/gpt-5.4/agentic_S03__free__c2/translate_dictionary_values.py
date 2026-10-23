from __future__ import annotations

from translation_client import azure_translate
from translation_models import (
    TranslationResult,
    normalize_dictionary_values,
    normalize_language_code,
)


def translate_dictionary_values(
    values: dict[str, object],
    source_language: str,
    target_language: str,
) -> dict[str, TranslationResult]:
    normalized = normalize_dictionary_values(values)
    keys = list(normalized.keys())
    payload = azure_translate(
        texts=[normalized[key] for key in keys],
        source_language=normalize_language_code(source_language),
        target_language=normalize_language_code(target_language),
        text_type="plain",
    )
    results: dict[str, TranslationResult] = {}
    for key, item in zip(keys, payload):
        translation = item["translations"][0]
        results[key] = TranslationResult(
            text=translation["text"],
            provider="azure-ai-translator",
            source_language=normalize_language_code(source_language),
            target_language=normalize_language_code(target_language),
            detected_language=item.get("detectedLanguage", {}).get("language"),
            raw=item,
        )
    return results
