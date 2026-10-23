import os
from google.cloud import translate_v2 as translate

def translate_caption(text: str, target_language: str = "fr") -> str:
    """
    Translates a live caption into another language using Google Cloud Translate.

    Requires the GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    
    Args:
        text: The caption text to translate.
        target_language: The ISO 639-1 code for the target language.
    
    Returns:
        The translated text.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)
    
    return result["translatedText"]
