import os
from google.cloud import translate_v2 as translate

def translate_invoice_note(text: str, target_language: str = "en") -> str:
    """Translate extracted invoice notes or descriptions using Google Cloud Translation."""
    # Google Cloud Translation automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # if set, or other standard authentication methods.
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
