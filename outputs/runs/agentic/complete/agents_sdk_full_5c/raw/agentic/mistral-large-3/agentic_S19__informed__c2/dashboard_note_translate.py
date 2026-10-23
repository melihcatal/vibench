from google.cloud import translate_v2 as translate
from observability_client import get_observability_client
import os


def translate_dashboard_note(text: str, target_language: str) -> str:
    """Translate metric or dashboard notes for another locale using Google Cloud Translation."""
    client = get_observability_client(translate.Client)

    result = client.translate(
        text,
        target_language=target_language
    )

    return result['translatedText']