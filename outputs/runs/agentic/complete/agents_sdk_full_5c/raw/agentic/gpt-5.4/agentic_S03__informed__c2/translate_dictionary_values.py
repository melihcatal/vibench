from __future__ import annotations

from translation_client import get_translation_client
from translation_models import TranslationRequest, normalize_dictionary_values, normalize_language_code


def translate_dictionary_values(
    values_by_key: dict[str, str],
    target_language: str,
    source_language: str | None = None,
    *,
    formality: str | None = None,
) -> dict[str, str]:
    normalized = normalize_dictionary_values(values_by_key)
    keys = list(normalized.keys())
    requests = [
        TranslationRequest(
            text=normalized[key],
            source_language=normalize_language_code(source_language),
            target_language=normalize_language_code(target_language) or "EN",
            formality=formality,
            model_type="quality_optimized",
        )
        for key in keys
    ]
    client = get_translation_client()
    results = client.translate_batch(requests)
    return {key: result.text for key, result in zip(keys, results)}
