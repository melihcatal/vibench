import os
from typing import Optional
from google.cloud import translate_v2 as translate


def translate_text(
    text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    """
    Translate a single text string between languages using Google Cloud Translation API.

    Args:
        text: The text to translate
        target_language: Target language code (e.g., 'es', 'fr', 'de')
        source_language: Optional source language code (e.g., 'en')

    Returns:
        Translated text string
    """
    client = translate.Client()

    if source_language:
        result = client.translate(
            text, target_language=target_language, source_language=source_language
        )
    else:
        result = client.translate(text, target_language=target_language)

    return result["translatedText"]
