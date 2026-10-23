from __future__ import annotations

from typing import Any, Dict

from batch_translate import batch_translate
from translation_models import BatchTranslationRequest, ensure_string_dict


def translate_dictionary_values(
    values: Dict[str, Any],
    target_language: str,
    source_language: str | None = None,
) -> Dict[str, str]:
    normalized = ensure_string_dict(values)
    keys = list(normalized.keys())
    results = batch_translate(
        BatchTranslationRequest(
            texts=[normalized[key] for key in keys],
            source_language=source_language,
            target_language=target_language,
        )
    )
    return {key: result.text for key, result in zip(keys, results)}
