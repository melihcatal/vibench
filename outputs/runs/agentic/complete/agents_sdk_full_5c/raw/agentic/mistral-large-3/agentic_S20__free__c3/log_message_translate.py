from google.cloud import translate_v2 as translate
import os


def translate_log_message(text: str, target_language: str = "es") -> str:
    """Translate log messages using Google Cloud Translation API."""
    client = translate.Client()
    
    result = client.translate(
        text, target_language=target_language
    )
    
    return result["translatedText"]