from google.cloud import translate_v2 as translate
import os
from typing import Dict, Any

# Provider-specific: Google Cloud Translation
client = translate.Client()


def translate_invoice_note(text: str, target_language: str = "en") -> str:
    """
    Translate extracted invoice notes or descriptions using Google Cloud Translation.
    """
    if not text:
        return ""

    result = client.translate(text, target_language=target_language)

    return result["translatedText"]
