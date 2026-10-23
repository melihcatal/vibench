from google.cloud import translate_v2 as translate
import os


def translate_invoice_note(text: str, target_language: str = "en") -> str:
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
