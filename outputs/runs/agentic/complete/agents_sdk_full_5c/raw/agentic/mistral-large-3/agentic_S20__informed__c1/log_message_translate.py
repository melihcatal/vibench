import os
from google.cloud import translate_v2 as translate

client = translate.Client()


def translate_log_message(text: str, target_language: str) -> str:
    """Translate support-visible log messages to another locale using Google Cloud Translation."""
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]