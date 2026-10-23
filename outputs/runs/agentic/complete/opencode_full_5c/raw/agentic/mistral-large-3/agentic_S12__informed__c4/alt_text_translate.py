from google.cloud import translate_v2 as translate
import os
from typing import Dict


def translate_alt_text(text: str, target_language: str) -> str:
    """Translates generated image descriptions using Google Cloud Translation API."""
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
