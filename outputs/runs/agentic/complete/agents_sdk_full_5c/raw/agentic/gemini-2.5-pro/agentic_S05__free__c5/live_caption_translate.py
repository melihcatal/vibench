import os
from google.cloud import translate_v2 as translate

def translate_live_caption(text: str, target_language: str) -> str:
    """
    Translates a live caption text chunk into the target language.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'fr', 'de').

    Returns:
        The translated text.
    """
    # The client uses Application Default Credentials by default.
    # Ensure you have authenticated via `gcloud auth application-default login`
    translate_client = translate.Client()

    if not text:
        return ""

    # The result is a dictionary, the translated text is in the 'translatedText' key.
    result = translate_client.translate(text, target_language=target_language)
    
    return result["translatedText"]
