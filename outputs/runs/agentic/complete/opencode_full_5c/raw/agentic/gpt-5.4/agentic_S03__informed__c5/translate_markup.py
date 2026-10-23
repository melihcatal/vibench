from __future__ import annotations

from translation_client import translate_text_items
from translation_models import TranslationRequest, TranslationResult, normalize_text


def translate_markup(request: TranslationRequest) -> TranslationResult:
    result = translate_text_items(
        texts=[normalize_text(request.text)],
        source_language=request.source_language,
        target_language=request.target_language,
        tag_handling="html",
    )
    return result.translations[0]
