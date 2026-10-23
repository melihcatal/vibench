import os
from google.cloud import translate_v2 as translate

def translate_compliance_note(text: str, target_language: str = 'es') -> str:
    """
    Translates encryption or compliance notes for reviewers using Google Cloud Translation.

    Args:
        text: The compliance note text to translate.
        target_language: The target language code (e.g., 'es' for Spanish).

    Returns:
        The translated text.
    """
    # Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set
    # or authenticated via `gcloud auth application-default login`
    translate_client = translate.Client()

    response = translate_client.translate(
        text,
        target_language=target_language
    )
    return response['translatedText']
