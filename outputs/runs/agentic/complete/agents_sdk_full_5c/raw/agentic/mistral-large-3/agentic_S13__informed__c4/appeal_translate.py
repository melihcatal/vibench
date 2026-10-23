"""
Translate appeal text for review using Google Cloud Translation.
"""
from google.cloud import translate_v2 as translate
import os


def translate_appeal(text: str, target_language: str = "en") -> str:
    """Translate appeal text using Google Cloud Translation."""
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]