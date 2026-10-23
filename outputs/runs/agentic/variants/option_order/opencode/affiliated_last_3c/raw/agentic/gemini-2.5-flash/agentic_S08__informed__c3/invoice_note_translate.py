import os
from google.cloud import translate_v2 as translate


def translate_text(text: str, target_language: str = "en") -> str:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]


def translate_invoice_note(note: str, target_language: str = "en") -> str:
    return translate_text(note, target_language)
