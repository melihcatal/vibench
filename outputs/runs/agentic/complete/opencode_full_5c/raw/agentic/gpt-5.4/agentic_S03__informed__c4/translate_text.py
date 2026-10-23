from __future__ import annotations

from translation_client import GOOGLE_TRANSLATE_MODEL, translate_texts
from translation_models import (
    TranslationRequest,
    TranslationResult,
    build_translation_result,
    normalize_text,
)


def translate_text(request: TranslationRequest) -> TranslationResult:
    payload = translate_texts(
        texts=[normalize_text(request.text)],
        source_language=request.source_language,
        target_language=request.target_language,
        mime_type=request.mime_type,
    )
    result = build_translation_result(
        payload["translations"][0], provider=payload["provider"]
    )
    result.model = GOOGLE_TRANSLATE_MODEL
    return result
