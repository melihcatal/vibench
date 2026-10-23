from google.cloud import translate_v2 as translate
import os
from typing import Dict, Any


def payload_translate(text: str, target_language: str) -> str:
    """
    Translates customer-facing message payload text using Google Cloud Translation.

    Args:
        text: Text to translate.
        target_language: Target language code (e.g., 'es', 'fr').

    Returns:
        Translated text.
    """
    client = translate.Client()

    result = client.translate(text, target_language=target_language)

    return result["translatedText"]
