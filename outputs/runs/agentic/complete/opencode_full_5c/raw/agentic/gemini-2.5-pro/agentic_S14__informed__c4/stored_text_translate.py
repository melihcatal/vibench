import os
from google.cloud import translate_v2 as translate


def translate_text_google(
    text: str, target_language: str, source_language: str = ""
) -> dict:
    """
    Translates text using the Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language (optional).

    Returns:
        A dictionary containing the translated text and detected source language.
    """
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return result
