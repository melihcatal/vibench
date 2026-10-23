import os
from google.cloud import translate_v2 as translate


def translate_alt_text(text: str, target_language: str = "es") -> str:
    """
    Translates generated image descriptions using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
