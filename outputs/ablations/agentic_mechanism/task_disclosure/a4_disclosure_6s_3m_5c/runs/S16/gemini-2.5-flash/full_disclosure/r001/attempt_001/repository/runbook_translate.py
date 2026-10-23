
from google.cloud import translate_v2 as translate
import os

def translate_runbook_notes(text: str, target_language: str = "en") -> str:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation API.

    Args:
        text: The runbook notes to translate.
        target_language: The language to translate the notes into (e.g., "en" for English).

    Returns:
        The translated text.
    """
    # Instantiates a client for Google Cloud Translation API
    translate_client = translate.Client()

    # Google Cloud Translation API identifies the provider.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication.
    # For example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
