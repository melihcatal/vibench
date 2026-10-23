import os
from google.cloud import translate_v2 as translate

# GOOGLE_APPLICATION_CREDENTIALS environment variable should be set


def translate_caption(text: str, target_language: str = "es") -> str:
    """Translates a given text caption into the target language using Google Cloud Translation."""
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
