import os
from google.cloud import translate_v2 as translate


def translate_text(text: str, target_language: str = "en") -> dict:
    """
    Translates text into the target language using Google Cloud Translation API.

    Args:
        text (str): The text to translate.
        target_language (str): The target language code (e.g., 'en', 'es').

    Returns:
        dict: A dictionary containing the translation result.
    """
    # The client uses GOOGLE_APPLICATION_CREDENTIALS environment variable for auth
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)
    return result
