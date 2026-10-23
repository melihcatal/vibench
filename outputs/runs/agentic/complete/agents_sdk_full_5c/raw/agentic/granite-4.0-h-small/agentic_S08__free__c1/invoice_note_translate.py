import os
from google.cloud import translate_v2 as translate

def invoice_note_translate(text: str, target_lang: str = "en") -> str:
    """
    Translate extracted invoice notes/description to target language using Google Cloud Translate.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_lang)
    return result["translatedText"]
