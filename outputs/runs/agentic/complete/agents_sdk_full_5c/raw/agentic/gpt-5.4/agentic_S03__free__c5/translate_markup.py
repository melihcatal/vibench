from __future__ import annotations

from translation_client import translate_with_google
from translation_models import TranslationRequest, TranslationResult


def translate_markup(
    markup_text: str,
    target_language: str,
    source_language: str | None = None,
) -> TranslationResult:
    request = TranslationRequest(
        text=markup_text,
        source_language=source_language,
        target_language=target_language,
        content_type="text/html",
    )
    raw = translate_with_google(
        text=request.text,
        target_language=request.target_language,
        source_language=request.source_language,
        format_="html",
    )
    return TranslationResult(
        translated_text=raw["translatedText"],
        detected_source_language=raw.get("detectedSourceLanguage") or request.source_language,
        provider="google_translate",
        model="google-cloud-translate-v2",
        raw=raw,
    )
