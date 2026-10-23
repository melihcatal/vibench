from __future__ import annotations

from google.cloud import translate_v2 as translate

from document_models import TranslationResult


def translate_ocr_text(text: str, target_language: str = "en") -> TranslationResult:
    client = translate.Client()
    response = client.translate(text, target_language=target_language)
    return TranslationResult(
        translated_text=response["translatedText"],
        source_language=response.get("detectedSourceLanguage"),
        target_language=target_language,
    )
