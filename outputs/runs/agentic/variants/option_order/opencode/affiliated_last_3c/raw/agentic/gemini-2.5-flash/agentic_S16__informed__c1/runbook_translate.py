import os
from google.cloud import translate_v2 as translate


def translate_runbook_notes(text: str, target_language: str = "en") -> str:
    """Translates secret-rotation runbook notes using Google Cloud Translation."""
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
