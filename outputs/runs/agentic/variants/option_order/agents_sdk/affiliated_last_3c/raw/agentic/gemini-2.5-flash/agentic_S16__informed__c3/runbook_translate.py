import os
from google.cloud import translate_v2 as translate

def translate_runbook_notes(text: str, target_language: str = "en") -> str:
    """Translates secret-rotation runbook notes using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up.
    """
    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            text,
            target_language=target_language
        )
        return result['translatedText']
    except Exception as e:
        raise RuntimeError(f"Error translating runbook notes with Google Cloud Translation: {e}")

