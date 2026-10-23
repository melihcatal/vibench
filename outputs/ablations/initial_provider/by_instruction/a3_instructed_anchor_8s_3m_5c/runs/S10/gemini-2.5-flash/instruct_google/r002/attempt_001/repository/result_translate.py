import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translates the given text to the target language using Google Cloud Translation.
    """
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
