import os
from google.cloud import translate_v2 as translate


def translate_runbook_notes(text: str, target_language: str = "es") -> str:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is expected for authentication
    translate_client = translate.Client()

    try:
        response = translate_client.translate(text, target_language=target_language)
        return response["translatedText"]
    except Exception as e:
        raise RuntimeError(
            f"Failed to translate runbook notes using Google Cloud Translation: {e}"
        )
