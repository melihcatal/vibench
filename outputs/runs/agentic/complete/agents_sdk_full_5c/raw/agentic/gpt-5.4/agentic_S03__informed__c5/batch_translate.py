from __future__ import annotations

from typing import List, Optional, Sequence

from translation_client import ensure_non_empty_texts, get_translation_client
from translation_models import BatchTranslationRequest, TranslationResult


def batch_translate(
    texts: Sequence[str],
    target_language: str,
    source_language: Optional[str] = None,
) -> List[TranslationResult]:
    client = get_translation_client()
    request = BatchTranslationRequest(
        texts=ensure_non_empty_texts(texts),
        source_language=source_language,
        target_language=target_language,
        text_type="plain",
    )
    return client.translate_batch(request)
