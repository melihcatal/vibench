from __future__ import annotations

from typing import Optional, Sequence

from translation_client import get_translation_client
from translation_models import BatchTranslationRequest, BatchTranslationResult, normalize_text_list


def batch_translate(
    texts: Sequence[str],
    target_language: str,
    source_language: Optional[str] = None,
) -> BatchTranslationResult:
    client = get_translation_client()
    request = BatchTranslationRequest(
        texts=normalize_text_list(texts),
        source_language=source_language,
        target_language=target_language,
    )
    translations = client.translate_batch(
        list(request.texts),
        target_language=request.target_language,
        source_language=request.source_language,
        preserve_formatting=request.preserve_formatting,
    )
    return BatchTranslationResult(translations=translations, provider="DeepL")
