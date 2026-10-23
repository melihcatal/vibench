from __future__ import annotations

from translation_client import DEEPL_MODEL, DEEPL_PROVIDER, translate_text_with_deepl
from translation_models import TranslationRequest, TranslationResult


def translate_text(request: TranslationRequest) -> TranslationResult:
    response = translate_text_with_deepl(
        text=request.text,
        source_language=request.source_language,
        target_language=request.target_language,
    )
    return TranslationResult(
        text=response.text,
        detected_source_language=getattr(response, "detected_source_lang", None),
        provider=DEEPL_PROVIDER,
        model=DEEPL_MODEL,
        raw_response=response,
    )
