from __future__ import annotations

from translation_client import translate_text_with_deepl
from translation_models import TranslationRequest


def translate_markup(
    markup: str,
    target_language: str,
    source_language: str | None = None,
    formality: str | None = None,
) -> str:
    request = TranslationRequest(
        text=markup,
        source_language=source_language,
        target_language=target_language,
        formality=formality,
    )
    return (
        translate_text_with_deepl(request).raw.text
        if hasattr(translate_text_with_deepl(request).raw, "text")
        else translate_text_with_deepl(request).text
    )
