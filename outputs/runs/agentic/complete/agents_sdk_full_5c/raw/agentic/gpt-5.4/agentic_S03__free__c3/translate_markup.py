from __future__ import annotations

from translation_client import get_deepl_client
from translation_models import TranslationRequest, TranslationResult, normalize_language_code


def translate_markup(request: TranslationRequest) -> TranslationResult:
    client = get_deepl_client()
    response = client.translate_text(
        request.text,
        source_lang=normalize_language_code(request.source_language),
        target_lang=normalize_language_code(request.target_language),
        tag_handling="html",
        glossary=request.glossary_id,
    )
    return TranslationResult(
        translated_text=response.text,
        detected_source_language=getattr(response, "detected_source_lang", None),
        provider="deepl",
        raw={
            "tag_handling": "html",
            "billed_characters": getattr(response, "billed_characters", None),
        },
    )
