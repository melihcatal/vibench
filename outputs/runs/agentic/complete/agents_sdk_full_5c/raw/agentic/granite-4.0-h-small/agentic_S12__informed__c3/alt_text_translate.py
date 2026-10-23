# alt_text_translate.py
import os
from typing import Optional
from google.cloud import translate_v2 as translate

# Use Google Cloud Translation client (credentials via GOOGLE_APPLICATION_CREDENTIALS env var)
translate_client = translate.Client()


def alt_text_translate(description: str, target_language: str = "es") -> Optional[str]:
    """Translate the generated image description into another language."""
    if not description:
        return None
    result = translate_client.translate(description, target_language=target_language)
    return result.get("translatedText")
