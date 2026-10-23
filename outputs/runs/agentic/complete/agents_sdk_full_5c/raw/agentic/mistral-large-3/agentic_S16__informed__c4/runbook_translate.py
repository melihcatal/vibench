from google.cloud import translate_v2 as translate
import os


def translate_runbook_notes(text: str, target_language: str = "es") -> str:
    """
    Translate secret-rotation runbook notes using Google Cloud Translation.
    
    Args:
        text: The text to translate.
        target_language: Target language code (e.g., "es", "fr").
    
    Returns:
        Translated text.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]