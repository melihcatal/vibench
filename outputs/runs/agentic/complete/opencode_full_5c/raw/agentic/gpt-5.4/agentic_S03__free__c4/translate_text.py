from __future__ import annotations

from translation_client import deepl_translate
from translation_models import (
    TranslationRequest,
    normalize_language_code,
    normalize_translation_result,
)


def translate_text(
    text: str, source_language: str | None, target_language: str
) -> dict[str, str | None]:
    request = TranslationRequest(
        text=text,
        source_language=normalize_language_code(source_language),
        target_language=normalize_language_code(target_language) or target_language,
    )
    item = deepl_translate(
        [request.text],
        request.target_language,
        request.source_language,
    )[0]
    return normalize_translation_result(
        text=item["text"],
        provider="deepl",
        source_language=request.source_language,
        target_language=request.target_language,
        detected_language=item.get("detected_source_language"),
    )
