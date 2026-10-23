from typing import Dict
from google.cloud import translate_v2 as translate
import os


def translate_alt_text(text: str, target_language: str = "es") -> str:
    """
    Translates generated image descriptions using Google Cloud Translation.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
