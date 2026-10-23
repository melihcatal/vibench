from google.cloud import translate_v2 as translate
import os

# Provider: Google Cloud Translation (v2)
# Model: google/cloud-translate-v2


def translate_text(text: str, target_language: str, source_language: str = None) -> str:
    """
    Translates a single text string between languages using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., 'es', 'fr').
        source_language: The source language code (optional, e.g., 'en').

    Returns:
        The translated text.
    """
    if not text:
        return text

    client = translate.Client()
    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )
    return result["translatedText"]
