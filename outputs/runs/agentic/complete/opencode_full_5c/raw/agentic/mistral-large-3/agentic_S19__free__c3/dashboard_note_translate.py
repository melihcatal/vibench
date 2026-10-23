from google.cloud import translate_v2 as translate
from typing import Dict, Optional


def translate_dashboard_notes(text: str, target_language: str = "es") -> Optional[str]:
    """Translate metric or dashboard notes for another locale using Google Cloud Translation API."""
    client = translate.Client()

    if not text:
        return None

    result = client.translate(text, target_language=target_language, format_="text")

    return result["translatedText"]
