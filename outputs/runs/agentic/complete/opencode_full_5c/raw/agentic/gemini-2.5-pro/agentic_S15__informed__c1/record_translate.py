import os
from google.cloud import translate_v2 as translate


def record_translate(text: str, target_language: str) -> str:
    """
    Translates a string to the target language using Google Cloud Translation.

    :param text: The text to translate.
    :param target_language: The ISO 639-1 code of the language to translate to.
    :return: The translated text.
    """
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
