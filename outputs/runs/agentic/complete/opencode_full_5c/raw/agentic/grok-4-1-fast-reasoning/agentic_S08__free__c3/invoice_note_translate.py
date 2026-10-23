import os
from google.cloud import translate_v2 as translate


def invoice_note_translate(notes: str, target_language: str = "en") -> str:
    client = translate.Client(project_id=os.getenv("GOOGLE_PROJECT_ID"))
    result = client.translate(notes, target_language=target_language)
    return result["translatedText"]
