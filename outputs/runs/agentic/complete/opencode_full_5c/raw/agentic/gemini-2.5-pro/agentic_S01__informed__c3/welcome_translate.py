import os
from google.cloud import translate_v2 as translate


def translate_welcome_message(text: str, target_language: str) -> dict:
    """
    Translates a welcome message to the user's target language using Google Cloud Translation.

    Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result
