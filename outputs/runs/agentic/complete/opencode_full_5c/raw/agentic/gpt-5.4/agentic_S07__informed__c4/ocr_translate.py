from __future__ import annotations

import deepl

from document_models import TranslationResult


def translate_ocr_text(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    translator = deepl.Translator()
    response = translator.translate_text(
        text,
        source_lang=source_language,
        target_lang=target_language,
    )
    detected_source = getattr(response, "detected_source_lang", source_language)
    return TranslationResult(
        translated_text=str(response.text),
        source_language=detected_source,
        target_language=target_language,
        provider="deepl",
        raw=response,
    )
