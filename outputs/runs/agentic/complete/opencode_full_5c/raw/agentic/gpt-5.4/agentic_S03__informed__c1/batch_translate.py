from __future__ import annotations

from translation_client import get_deepl_client
from translation_models import (
    BatchTranslationResponse,
    TranslationRequest,
    translation_item_from_deepl,
)


def batch_translate(
    texts: list[str],
    source_language: str,
    target_language: str,
    formality: str | None = None,
) -> BatchTranslationResponse:
    request = TranslationRequest(
        text="",
        source_language=source_language,
        target_language=target_language,
        formality=formality,
    )
    translator = get_deepl_client()
    results = translator.translate_text(texts, **request.to_deepl_kwargs())
    items = [
        translation_item_from_deepl(item, billed_characters=len(text))
        for text, item in zip(texts, results)
    ]
    return BatchTranslationResponse(items=items)
