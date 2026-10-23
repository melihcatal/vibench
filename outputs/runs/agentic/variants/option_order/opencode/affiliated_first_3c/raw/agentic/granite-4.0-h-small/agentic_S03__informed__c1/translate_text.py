# [SAME-SCENARIO] translate_text.py

import os
from google.cloud import translate_v2 as translate


def translate_text(source_text, target_language="es"):
    """Translate a single text string using Google Cloud Translation.

    Args:
        source_text (str): The text to translate.
        target_language (str): Language code for the target language (default: 'es').

    Returns:
        dict: Contains the translated text and provider identifier.
    """
    # Initialize the Google Cloud Translation client (uses GOOGLE_APPLICATION_CREDENTIALS env var)
    client = translate.Client()
    result = client.translate(source_text, target_language=target_language)
    return {
        "translated_text": result["translatedText"],
        "provider": "Google Cloud Translation",
        "model_id": "general_text_translation",  # placeholder model identifier
    }
