from google.cloud import translate_v2 as translate
import os


def dashboard_note_translate(text: str, target_language: str = "es") -> str:
    """Translate metric or dashboard notes for another locale using Google Cloud Translation."""
    client = translate.Client()
    
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]