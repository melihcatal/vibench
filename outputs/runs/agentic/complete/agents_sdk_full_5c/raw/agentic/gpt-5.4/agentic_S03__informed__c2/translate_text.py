from __future__ import annotations

from translation_client import get_translation_client
from translation_models import TranslationRequest, normalize_language_code


def translate_text(
    text: str,
    target_language: str,
    source_language: str | None = None,
    *,
    formality: str | None = None,
    context: str | None = None,
    glossary_id: str | None = None,
) -> str:
    client = get_translation_client()
    request = TranslationRequest(
        text=text,
        source_language=normalize_language_code(source_language),
        target_language=normalize_language_code(target_language) or "EN",
        formality=formality,
        context=context,
        glossary_id=glossary_id,
        model_type="quality_optimized",
    )
    return client.translate(request).text
