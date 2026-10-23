"""
Translate appeal text for review using Google Cloud Translation API.
"""
import os
from typing import List
from google.cloud import translate_v2 as translate


def translate_appeal(text: str, target_language: str = "en") -> str:
    """Translate appeal text to the target language using Google Cloud Translation API."""
    client = translate.Client()
    if not client:
        raise ValueError("Google Cloud Translation API credentials are required.")

    result = client.translate(text, target_language=target_language)
    return result['translatedText']