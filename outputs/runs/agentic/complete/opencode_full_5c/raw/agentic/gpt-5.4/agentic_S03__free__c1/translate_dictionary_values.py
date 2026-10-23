from __future__ import annotations

from typing import Mapping, Optional

from translation_client import DeepLTranslationClient
from translation_models import (
    BatchTranslationRequest,
    extract_dictionary_values,
    merge_dictionary_values,
    normalize_deepl_translation_response,
)


def translate_dictionary_values(
    data: Mapping[str, object],
    target_language: str,
    source_language: Optional[str] = None,
) -> dict[str, str]:
    client = DeepLTranslationClient()
    values = extract_dictionary_values(data)
    request = BatchTranslationRequest(
        texts=values,
        source_language=source_language,
        target_language=target_language,
    )
    response = client.translate(request.to_deepl_payload())
    normalized = normalize_deepl_translation_response(response)
    return merge_dictionary_values(data, normalized.translations)
