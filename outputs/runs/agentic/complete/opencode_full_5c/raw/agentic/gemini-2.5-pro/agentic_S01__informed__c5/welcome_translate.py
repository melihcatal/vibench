import os
from google.cloud import translate_v2 as translate


def translate_welcome_message(text: str, target_language: str) -> str:
    """
    Translates a welcome message to the user's target locale using
    Google Cloud Translation.
    """
    # GOOGLE_APPLICATION_CREDENTIALS must be set in the environment
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
