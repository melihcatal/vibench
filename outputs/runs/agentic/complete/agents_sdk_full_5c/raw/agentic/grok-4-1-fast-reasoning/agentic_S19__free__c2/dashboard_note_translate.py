from google.cloud import translate_v2
from typing import Optional

def dashboard_note_translate(note: str, target_language: str = "fr") -> str:
    client = translate_v2.Client()
    result = client.translate(note, target_language=target_language)
    return result["translatedText"]
