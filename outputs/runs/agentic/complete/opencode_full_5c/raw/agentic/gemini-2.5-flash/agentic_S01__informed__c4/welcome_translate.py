import os
from google.cloud import translate_v2 as translate


def welcome_translate(text: str, target_language: str) -> str:
    """Translates onboarding copy into the user's locale using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., 'es' for Spanish).

    Returns:
        The translated text.
    """
    # Google Cloud Translation automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # if set in the environment or other standard credential locations.
    # Ensure the GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # to the path of your service account key file.

    translate_client = translate.Client()

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        raise RuntimeError(f"Google Cloud Translation failed: {e}")
