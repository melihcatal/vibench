import os
from google.cloud import translate_v2 as translate


def translate_runbook_notes(text: str, target_language: str = "en") -> str:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up for authentication.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set, or authenticate via other means
    # The client will automatically pick up credentials from the environment.
    # For local testing, ensure your GOOGLE_APPLICATION_CREDENTIALS points to a valid service account key file.
    # For deployed environments, use Workload Identity or similar.

    translate_client = translate.Client()

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        raise
