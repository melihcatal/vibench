from __future__ import annotations

from google.cloud import translate_v2 as translate

from speech_models import TranslationResult


GOOGLE_TRANSLATE_PROVIDER = "translate.googleapis.com"


def translate_script(text: str, target_language: str, source_language: str | None = None) -> TranslationResult:
    client = translate.Client()
    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        format_="text",
    )
    return TranslationResult(
        translated_text=result["translatedText"],
        source_language=result.get("detectedSourceLanguage") or source_language,
        target_language=target_language,
    )
