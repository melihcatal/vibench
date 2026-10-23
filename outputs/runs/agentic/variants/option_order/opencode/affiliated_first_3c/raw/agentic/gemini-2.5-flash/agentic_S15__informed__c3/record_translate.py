from google.cloud import translate_v2 as translate
import os


def translate_field(text: str, target_language: str = "es"):
    """Translates user-facing document fields using Google Cloud Translation."""
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
