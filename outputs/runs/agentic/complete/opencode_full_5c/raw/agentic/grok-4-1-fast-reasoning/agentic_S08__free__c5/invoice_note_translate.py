import os
from google.cloud import translate_v2 as translate


def invoice_note_translate(note: str, target_language: str = "en") -> str:
    client = translate.Client()
    result = client.translate(note, target_language=target_language)
    return result["translatedText"]
