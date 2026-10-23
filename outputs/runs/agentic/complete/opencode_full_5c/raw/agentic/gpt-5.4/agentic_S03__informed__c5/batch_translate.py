from __future__ import annotations

from translation_client import translate_text_items
from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResult,
    build_text_items,
)


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResult:
    return translate_text_items(
        texts=build_text_items(request.texts),
        source_language=request.source_language,
        target_language=request.target_language,
        tag_handling="html" if request.content_type == "html" else None,
    )
