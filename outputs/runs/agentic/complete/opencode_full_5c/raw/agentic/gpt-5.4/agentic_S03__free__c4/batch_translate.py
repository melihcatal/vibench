from __future__ import annotations

from translation_client import deepl_translate
from translation_models import (
    BatchTranslationRequest,
    ensure_text_list,
    normalize_language_code,
    normalize_translation_result,
)


def batch_translate(
    texts: list[str], source_language: str | None, target_language: str
) -> list[dict[str, str | None]]:
    request = BatchTranslationRequest(
        texts=ensure_text_list(texts),
        source_language=normalize_language_code(source_language),
        target_language=normalize_language_code(target_language) or target_language,
    )
    translations = deepl_translate(
        request.texts, request.target_language, request.source_language
    )
    return [
        normalize_translation_result(
            text=item["text"],
            provider="deepl",
            source_language=request.source_language,
            target_language=request.target_language,
            detected_language=item.get("detected_source_language"),
        )
        for item in translations
    ]
