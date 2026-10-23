from __future__ import annotations

from typing import List, Optional

from translation_client import DeepLTranslationClient
from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResult,
    normalize_deepl_translation_response,
)


def batch_translate(
    texts: List[str], target_language: str, source_language: Optional[str] = None
) -> BatchTranslationResult:
    client = DeepLTranslationClient()
    request = BatchTranslationRequest(
        texts=texts,
        source_language=source_language,
        target_language=target_language,
    )
    response = client.translate(request.to_deepl_payload())
    return normalize_deepl_translation_response(response)
