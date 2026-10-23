import os
from typing import Dict
from google.cloud import translate_v2 as translate


def translate_appeal(text: str, target_language: str = "en") -> str:
    """
    Translate appeal text for review using Google Cloud Translation.
    Returns translated text.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]