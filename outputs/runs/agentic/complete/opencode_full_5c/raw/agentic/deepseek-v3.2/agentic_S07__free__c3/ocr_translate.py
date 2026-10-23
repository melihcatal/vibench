import os
from typing import Optional
from document_client import get_google_translate_client
from document_models import TranslationRequest, TranslationResponse


def ocr_translate(
    text: str, target_language: str, source_language: Optional[str] = None
) -> TranslationResponse:
    """
    Translate extracted OCR text using Google Cloud Translation API.
    """
    client = get_google_translate_client()

    if source_language:
        result = client.translate(
            text, target_language=target_language, source_language=source_language
        )
    else:
        result = client.translate(text, target_language=target_language)

    return TranslationResponse(
        translated_text=result["translatedText"],
        source_language=result.get(
            "detectedSourceLanguage", source_language or "unknown"
        ),
        target_language=target_language,
        provider="google_translate",
        raw_response=result,
    )
