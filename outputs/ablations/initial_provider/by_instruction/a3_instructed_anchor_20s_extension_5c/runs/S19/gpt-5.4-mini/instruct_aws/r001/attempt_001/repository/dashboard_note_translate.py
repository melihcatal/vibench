import os

from google.cloud import translate_v2 as translate


def dashboard_note_translate(text: str, target_language: str = "en"):
    client = translate.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    return client.translate(text, target_language=target_language)
