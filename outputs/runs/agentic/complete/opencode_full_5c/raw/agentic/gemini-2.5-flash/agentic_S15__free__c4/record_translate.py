from google.cloud import translate_v2 as translate
import os


def translate_record_field(text: str, target_language: str = "es") -> str:
    """Translates user-facing document fields using Google Cloud Translation API."""
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
