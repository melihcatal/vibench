from __future__ import annotations

from typing import Dict, Mapping, Optional

from translation_client import get_translation_client
from translation_models import BatchTranslationRequest, normalize_mapping_values


def translate_dictionary_values(
    values: Mapping[str, object],
    target_language: str,
    source_language: Optional[str] = None,
) -> Dict[str, str]:
    normalized = normalize_mapping_values(values)
    keys = list(normalized.keys())
    client = get_translation_client()
    results = client.translate_batch(
        BatchTranslationRequest(
            texts=[normalized[key] for key in keys],
            source_language=source_language,
            target_language=target_language,
            text_type="plain",
        )
    )
    return {key: result.text for key, result in zip(keys, results)}
