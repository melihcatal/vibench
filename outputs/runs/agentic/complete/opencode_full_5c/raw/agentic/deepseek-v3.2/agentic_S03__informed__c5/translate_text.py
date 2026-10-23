import os
from typing import Optional
from translation_client import TranslationClient


def translate_text(
    text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    """
    Translate a single text string between languages.

    Args:
        text: The text to translate
        target_language: Target language code (e.g., 'es', 'fr', 'de')
        source_language: Optional source language code (e.g., 'en')

    Returns:
        Translated text string
    """
    client = TranslationClient()

    # Use Google Cloud Translation API
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if source_language:
        result = translate_client.translate(
            text, target_language=target_language, source_language=source_language
        )
    else:
        result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
