from __future__ import annotations

from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResult


def translate_text(
    text: str, source_language: str, target_language: str
) -> TranslationResult:
    request = TranslationRequest(
        text=text, source_language=source_language, target_language=target_language
    )
    payload = TranslationClient().translate(
        text=request.text,
        source_language=request.source_language,
        target_language=request.target_language,
    )
    return TranslationResult(
        text=payload["translatedText"],
        detected_source_language=payload.get("detectedSourceLanguage"),
        provider="google_translate",
    )
