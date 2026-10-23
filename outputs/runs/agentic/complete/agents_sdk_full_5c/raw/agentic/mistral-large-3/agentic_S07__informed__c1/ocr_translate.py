import os
from typing import Optional
from google.cloud import translate_v2 as translate
from document_models import TranslationResponse


def translate_text(text: str, target_language: str, source_language: Optional[str] = None) -> TranslationResponse:
    """
    Translate extracted OCR text using Google Cloud Translation.
    """
    client = translate.Client()

    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )

    return TranslationResponse(
        translated_text=result['translatedText'],
        source_language=result['detectedSourceLanguage'],
        target_language=target_language
    )