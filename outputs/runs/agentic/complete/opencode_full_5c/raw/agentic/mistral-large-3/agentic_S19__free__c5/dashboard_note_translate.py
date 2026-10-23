from google.cloud import translate_v2 as translate
from typing import List


def translate_text(texts: List[str], target_language: str = "es") -> List[str]:
    """Translate metric or dashboard notes using Google Cloud Translation API."""
    client = translate.Client()
    results = client.translate(texts, target_language=target_language)
    return [result["translatedText"] for result in results]


def dashboard_note_translate(notes: List[str], target_locale: str = "es") -> dict:
    """Translate metric or dashboard notes for another locale using Google Cloud Translation."""
    translated_notes = translate_text(notes, target_language=target_locale)
    return {
        "original_notes": notes,
        "translated_notes": translated_notes,
        "target_locale": target_locale,
    }
