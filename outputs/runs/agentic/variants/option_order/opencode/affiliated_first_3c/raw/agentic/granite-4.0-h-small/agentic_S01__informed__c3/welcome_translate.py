import os
from google.cloud import translate_v2 as translate

google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def translate_onboarding_copy(text, target_locale="en"):
    """Translate onboarding copy using Google Cloud Translation.
    Returns translated text string.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_locale)
    return result["translatedText"]
