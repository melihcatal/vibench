from typing import List, Optional
from google.cloud import translate_v2 as translate
from pydantic import BaseModel


class TranslationResult(BaseModel):
    translated_text: str
    detected_source_language: Optional[str] = None


def initialize_translation_client():
    """
    Initializes the Google Cloud Translation client.

    Returns:
        Configured Google Cloud Translation client.
    """
    return translate.Client()


def translate_query(query: str, target_language: str = "en") -> TranslationResult:
    """
    Translates a query into the target language using Google Cloud Translation API.

    Args:
        query: Input query text to translate.
        target_language: Target language code (e.g., "en" for English).

    Returns:
        TranslationResult containing the translated text and detected source language.
    """
    client = initialize_translation_client()

    result = client.translate(query, target_language=target_language)

    return TranslationResult(
        translated_text=result["translatedText"],
        detected_source_language=result.get("detectedSourceLanguage"),
    )
