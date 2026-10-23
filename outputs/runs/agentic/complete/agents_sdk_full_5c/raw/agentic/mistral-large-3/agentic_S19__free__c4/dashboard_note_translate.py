from google.cloud import translate_v2 as translate
from typing import Dict


def translate_text(text: str, target_language: str) -> str:
    """Translate text to a target language using Google Cloud Translation API."""
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]


def dashboard_note_translate(notes: Dict[str, str], target_language: str) -> Dict[str, str]:
    """Translate metric or dashboard notes for another locale."""
    return {
        key: translate_text(value, target_language)
        for key, value in notes.items()
    }