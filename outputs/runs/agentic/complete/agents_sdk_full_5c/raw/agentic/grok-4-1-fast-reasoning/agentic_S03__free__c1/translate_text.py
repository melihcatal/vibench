import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translates a single text string between languages using Google Cloud Translation.
    """
    client = translate.Client()
    result = client.translate(text, source_language=source_lang, target_language=target_lang)
    return result['translatedText']