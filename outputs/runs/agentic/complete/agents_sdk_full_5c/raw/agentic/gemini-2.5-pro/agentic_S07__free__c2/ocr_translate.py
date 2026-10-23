
from google.cloud import translate_v2 as translate
import os

def translate_text(text: str, target_language: str) -> str:
    """
    Translates text to a target language using Google Cloud Translate API.

    Requires Google Cloud credentials to be set up in the environment,
    e.g., by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code of the language to translate to (e.g., 'es', 'fr').

    Returns:
        The translated text.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
