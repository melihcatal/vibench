import os
from google.cloud import translate_v2 as translate

def translate_welcome_message(text: str, target_locale: str) -> str:
    """
    Translates text into the target locale using Google Cloud Translate.

    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    try:
        translate_client = translate.Client()
        result = translate_client.translate(text, target_language=target_locale)
        return result['translatedText']
    except Exception as e:
        # Handle exceptions from the Google Cloud client
        print(f"An error occurred with Google Cloud Translate: {e}")
        # Fallback to original text if translation fails
        return text
