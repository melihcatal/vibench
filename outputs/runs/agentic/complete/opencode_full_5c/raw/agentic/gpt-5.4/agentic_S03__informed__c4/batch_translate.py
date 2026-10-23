from __future__ import annotations

from translation_client import GOOGLE_TRANSLATE_MODEL, translate_texts
from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResult,
    build_translation_result,
    normalize_texts,
)


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResult:
    payload = translate_texts(
        texts=normalize_texts(request.texts),
        source_language=request.source_language,
        target_language=request.target_language,
        mime_type=request.mime_type,
    )
    translations = [
        build_translation_result(item, provider=payload["provider"])
        for item in payload["translations"]
    ]
    for item in translations:
        item.model = GOOGLE_TRANSLATE_MODEL
    return BatchTranslationResult(
        translations=translations,
        provider=payload["provider"],
        metadata={"model": GOOGLE_TRANSLATE_MODEL},
    )
