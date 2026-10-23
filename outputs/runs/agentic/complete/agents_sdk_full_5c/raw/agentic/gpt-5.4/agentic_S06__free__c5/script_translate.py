from __future__ import annotations

from google.cloud import translate_v2 as translate

from speech_models import TranslationResult


def translate_script(text: str, target_language_code: str, source_language_code: str | None = None) -> TranslationResult:
    client = translate.Client()
    response = client.translate(
        text,
        target_language=target_language_code,
        source_language=source_language_code,
        format_="text",
    )
    return TranslationResult(
        translated_text=response["translatedText"],
        source_language_code=response.get("detectedSourceLanguage") or source_language_code,
        target_language_code=target_language_code,
    )
