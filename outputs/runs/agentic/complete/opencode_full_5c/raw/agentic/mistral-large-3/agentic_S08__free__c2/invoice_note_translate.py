from typing import Optional
from google.cloud import translate_v2 as translate
import os


def translate_invoice_note(text: str, target_language: str = "en") -> Optional[str]:
    """Translate extracted invoice notes or descriptions using Google Cloud Translation API."""
    client = translate.Client()

    if not text:
        return None

    result = client.translate(text, target_language=target_language)

    return result["translatedText"]
