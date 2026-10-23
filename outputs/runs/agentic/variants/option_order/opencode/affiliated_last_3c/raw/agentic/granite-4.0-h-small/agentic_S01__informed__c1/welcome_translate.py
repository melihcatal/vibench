import os
from google.cloud import translate_v2 as translate

# Google Cloud Translation configuration from environment variables
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Initialize the Translation client
translate_client = translate.Client()


def translate_onboarding(text: str, target_locale: str) -> str:
    """Translates onboarding copy into the user's locale.

    Args:
        text: Original onboarding string.
        target_locale: Target locale code (e.g. 'es', 'fr').
    Returns the translated text.
    """
    result = translate_client.translate(text, target_language=target_locale)
    return result["translatedText"]
