import os
from google.cloud import translate_v2 as translate

def translate_dashboard_note(text: str, target_language: str = 'es') -> str:
    """
    Translates metric or dashboard notes for another locale using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code of the target language (e.g., 'es' for Spanish).

    Returns:
        The translated text.
    """
    # Google Cloud Translation automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # if set, or attempts to find credentials.
    translate_client = translate.Client()

    result = translate_client.translate(
        text,
        target_language=target_language
    )

    return result['translatedText']

