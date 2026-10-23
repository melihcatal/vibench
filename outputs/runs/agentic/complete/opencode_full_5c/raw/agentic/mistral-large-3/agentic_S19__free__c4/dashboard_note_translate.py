import os
from typing import Dict
from google.cloud import translate_v2 as translate


def translate_text(text: str, target_language: str = "es") -> str:
    """Translate text using Google Cloud Translation API."""
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]


def translate_dashboard_notes(notes: Dict[str, str], locale: str) -> Dict[str, str]:
    """Translate metric or dashboard notes for another locale."""
    return {key: translate_text(value, locale) for key, value in notes.items()}
