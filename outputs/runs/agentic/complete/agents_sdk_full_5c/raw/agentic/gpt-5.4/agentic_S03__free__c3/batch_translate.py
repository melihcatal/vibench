from __future__ import annotations

from translation_client import get_deepl_client
from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResult,
    TranslationResult,
    normalize_language_code,
    normalize_text_list,
)


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResult:
    client = get_deepl_client()
    texts = normalize_text_list(request.texts)
    responses = client.translate_text(
        texts,
        source_lang=normalize_language_code(request.source_language),
        target_lang=normalize_language_code(request.target_language),
        tag_handling=None,
        glossary=request.glossary_id,
    )
    translations = [
        TranslationResult(
            translated_text=item.text,
            detected_source_language=getattr(item, "detected_source_lang", None),
            provider="deepl",
            raw={
                "billed_characters": getattr(item, "billed_characters", None),
                "model_type_used": getattr(item, "model_type_used", None),
            },
        )
        for item in responses
    ]
    return BatchTranslationResult(
        translations=translations,
        provider="deepl",
        raw={"count": len(translations)},
    )
