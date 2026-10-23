import os
from google.cloud import translate_v2 as translate

def translate_onboarding_message(text: str, target_locale: str) -> str:
    """
    Translates a given text to a target locale using Google Cloud Translate.

    Args:
        text: The text to translate.
        target_locale: The ISO 639-1 language code of the target language.

    Returns:
        The translated text.
    """
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    # for this client to authenticate automatically.
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_locale)

    return result["translatedText"]
