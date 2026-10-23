import os

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

from google.cloud import translate_v2 as translate


def dashboard_note_translate(text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
