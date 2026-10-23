import os
from google.cloud import translate_v2 as translate
from typing import Optional

def translate_invoice_note(text: str, target_language: str = "en") -> Optional[str]:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "en" for English, "es" for Spanish).

    Returns:
        The translated text, or None if translation fails.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # default credentials are configured for Google Cloud.
    # The client will automatically pick up credentials from the environment.
    translate_client = translate.Client()

    if not text:
        return None

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        print(f"Error during translation: {e}")
        return None
