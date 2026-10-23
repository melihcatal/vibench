from __future__ import annotations

from translation_client import azure_translate
from translation_models import (
    TranslationRequest,
    TranslationResult,
    normalize_language_code,
)


def translate_markup(request: TranslationRequest) -> TranslationResult:
    source_language = normalize_language_code(request.source_language)
    target_language = normalize_language_code(request.target_language)
    payload = azure_translate(
        texts=[request.text],
        source_language=source_language,
        target_language=target_language,
        text_type="html",
    )[0]
    translation = payload["translations"][0]
    return TranslationResult(
        text=translation["text"],
        provider="azure-ai-translator",
        source_language=source_language,
        target_language=target_language,
        detected_language=payload.get("detectedLanguage", {}).get("language"),
        raw=payload,
    )
