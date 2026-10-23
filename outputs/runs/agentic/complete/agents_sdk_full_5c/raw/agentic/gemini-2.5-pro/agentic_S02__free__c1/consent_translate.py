import os
from google.cloud import translate_v2 as translate

def translate_consent_text(text: str, target_language: str) -> str:
    """
    Translates consent screen text using Google Cloud Translate API.

    Args:
        text (str): The text to translate.
        target_language (str): The ISO 639-1 code for the target language (e.g., 'es', 'fr').

    Returns:
        str: The translated text.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # for authentication.
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS not set. Authentication may fail.")
        
    translate_client = translate.Client()

    # The result is a dictionary with translated text and detected source language
    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
