import os
from google.cloud import translate_v2 as translate


def translate_caption(text: str, target_language: str) -> str:
    """Translates live captions into another language using Google Cloud Translation."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
