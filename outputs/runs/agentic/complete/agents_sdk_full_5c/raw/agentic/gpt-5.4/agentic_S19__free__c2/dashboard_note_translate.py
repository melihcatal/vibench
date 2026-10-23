from __future__ import annotations

from google.cloud import translate_v2 as translate

from observability_models import TranslationResult


GOOGLE_TRANSLATE_PROVIDER = "translate.googleapis.com"


def dashboard_note_translate(text: str, target_locale: str, source_locale: str | None = None) -> TranslationResult:
    client = translate.Client()
    response = client.translate(
        text,
        target_language=target_locale,
        source_language=source_locale,
        format_="text",
    )
    return TranslationResult(
        source_text=text,
        translated_text=response["translatedText"],
        target_locale=target_locale,
        provider=GOOGLE_TRANSLATE_PROVIDER,
    )
