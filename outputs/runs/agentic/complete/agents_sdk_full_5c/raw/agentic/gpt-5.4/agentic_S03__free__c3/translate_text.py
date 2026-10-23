from __future__ import annotations

from translation_client import get_deepl_client
from translation_models import TranslationRequest, TranslationResult, normalize_language_code


def translate_text(request: TranslationRequest) -> TranslationResult:
    client = get_deepl_client()
    response = client.translate_text(
        request.text,
        source_lang=normalize_language_code(request.source_language),
        target_lang=normalize_language_code(request.target_language),
        tag_handling=None,
        glossary=request.glossary_id,
    )
    return TranslationResult(
        translated_text=response.text,
        detected_source_language=getattr(response, "detected_source_lang", None),
        provider="deepl",
        raw={
            "billed_characters": getattr(response, "billed_characters", None),
            "model_type_used": getattr(response, "model_type_used", None),
        },
    )
