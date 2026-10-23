from __future__ import annotations

from translation_client import TranslationClient
from translation_models import TranslationResult


def translate_markup(
    markup: str, source_language: str, target_language: str
) -> TranslationResult:
    payload = TranslationClient().translate(
        text=markup,
        source_language=source_language,
        target_language=target_language,
        mime_type="text/html",
    )
    return TranslationResult(
        text=payload["translatedText"],
        detected_source_language=payload.get("detectedSourceLanguage"),
        provider="google_translate",
    )
