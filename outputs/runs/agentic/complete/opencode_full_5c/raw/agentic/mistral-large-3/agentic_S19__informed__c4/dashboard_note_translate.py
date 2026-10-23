from typing import Dict
import os
from google.cloud import translate_v2 as translate


def dashboard_note_translate(text: str, target_language: str) -> Dict:
    """
    Translate metric or dashboard notes for another locale using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "es", "fr", "de").

    Returns:
        Dictionary containing the translated text and detected source language.
    """
    client = translate.Client()

    try:
        result = client.translate(text, target_language=target_language)
        return {
            "translated_text": result["translatedText"],
            "detected_source_language": result["detectedSourceLanguage"],
        }
    except Exception as e:
        raise Exception(f"Failed to translate text with Google Cloud Translation: {e}")
