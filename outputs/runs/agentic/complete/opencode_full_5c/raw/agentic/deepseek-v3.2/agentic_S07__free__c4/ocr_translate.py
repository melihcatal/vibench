import os
from typing import Optional
from google.cloud import translate_v2 as translate
from document_client import get_google_client
from document_models import TranslationResult


def ocr_translate(
    text: str, target_language: str, source_language: Optional[str] = None
) -> TranslationResult:
    """
    Translate extracted OCR text using Google Cloud Translation API.

    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'es', 'fr', 'de')
        source_language: Optional source language code (auto-detected if not provided)

    Returns:
        TranslationResult containing original and translated text
    """
    client = get_google_client()

    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        format_="text",
    )

    detected_source = result.get("detectedSourceLanguage", source_language or "auto")

    return TranslationResult(
        original_text=text,
        translated_text=result["translatedText"],
        source_language=detected_source,
        target_language=target_language,
        provider="google_cloud_translate",
        model_id="google_translation_api",
        confidence=1.0,
    )
