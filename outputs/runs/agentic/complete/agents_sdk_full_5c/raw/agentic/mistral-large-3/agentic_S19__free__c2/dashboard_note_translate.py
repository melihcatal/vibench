from google.cloud import translate_v2 as translate
import os


def translate_dashboard_note(text: str, target_language: str = "es") -> str:
    """Translate metric or dashboard notes for another locale using Google Cloud Translation API."""
    client = translate.Client()
    if not isinstance(text, str) or not text.strip():
        return text

    result = client.translate(text, target_language=target_language)
    return result["translatedText"]