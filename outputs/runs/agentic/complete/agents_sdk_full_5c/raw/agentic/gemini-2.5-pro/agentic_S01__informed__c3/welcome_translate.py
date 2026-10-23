import os
from google.cloud import translate_v2 as translate

def translate_welcome_message(text: str, target_language: str) -> str:
    """
    Translates a welcome message to the user's target language using
    Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code for the target language.

    Returns:
        The translated text.
    """
    # GOOGLE_APPLICATION_CREDENTIALS env var is used automatically
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    
    return result['translatedText']
