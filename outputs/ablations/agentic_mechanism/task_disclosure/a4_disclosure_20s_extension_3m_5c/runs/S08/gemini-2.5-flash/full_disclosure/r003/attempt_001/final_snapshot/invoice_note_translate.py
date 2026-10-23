from google.cloud import translate_v2 as translate
import os

def translate_invoice_note(text: str, target_language: str = "en") -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation API.

    Args:
        text: The text to be translated.
        target_language: The target language for the translation (e.g., "en", "es", "fr").

    Returns:
        The translated text.
    """
    # Instantiates a client
    translate_client = translate.Client()

    # Google Cloud Translation API is identifiable by 'translate.Client()'
    # and the use of 'google.cloud.translate_v2'

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
