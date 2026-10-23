from google.cloud import translate_v2 as translate
import os


def translate_compliance_note(note: str, target_language: str = "es") -> str:
    client = translate.Client()
    result = client.translate(note, target_language=target_language)
    return result["translatedText"]
