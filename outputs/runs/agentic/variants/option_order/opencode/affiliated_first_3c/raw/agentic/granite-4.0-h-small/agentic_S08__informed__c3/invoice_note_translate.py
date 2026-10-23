import json
from google.cloud import translate_v2 as translate


def translate_invoice_notes(text: str, target_lang: str = "es") -> str:
    """Translates extracted invoice notes or descriptions using Google Cloud Translation.","""
    client = translate.Client()
    result = client.translate(text, target_language=target_lang)
    return result["translatedText"]
