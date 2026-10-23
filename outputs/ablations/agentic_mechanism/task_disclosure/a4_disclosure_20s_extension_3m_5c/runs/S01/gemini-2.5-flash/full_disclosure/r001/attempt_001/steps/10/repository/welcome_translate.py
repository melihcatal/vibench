from google.cloud import translate_v2 as translate
import os

def translate_onboarding_copy(text: str, target_language: str) -> str:
    """
    Translates onboarding copy into the user's locale using Google Cloud Translation.
    """
    # Initialize the Google Cloud Translation client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    translate_client = translate.Client()

    result = translate_client.translate(
        text,
        target_language=target_language
    )

    return result['translatedText']

