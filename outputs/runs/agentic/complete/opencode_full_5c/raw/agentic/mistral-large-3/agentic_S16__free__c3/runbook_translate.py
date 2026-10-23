from google.cloud import translate_v2 as translate
import os


def translate_runbook_notes(
    project_id: str, text: str, target_language: str = "es"
) -> str:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation API.

    Args:
        project_id: Google Cloud project ID.
        text: Text to translate.
        target_language: Target language code (defaults to "es" for Spanish).

    Returns:
        Translated text as a string.
    """
    client = translate.Client(project=project_id)
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
