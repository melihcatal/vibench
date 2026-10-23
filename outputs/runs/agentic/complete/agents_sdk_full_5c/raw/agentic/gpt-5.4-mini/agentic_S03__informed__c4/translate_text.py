from __future__ import annotations

from translation_client import translate_text as deepl_translate_text
from translation_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    translated_text = deepl_translate_text(
        request.text,
        request.source_language,
        request.target_language,
        glossary=dict(request.glossary or {}),
        formality=request.formality,
    )
    return TranslationResponse(translated_text=translated_text)
