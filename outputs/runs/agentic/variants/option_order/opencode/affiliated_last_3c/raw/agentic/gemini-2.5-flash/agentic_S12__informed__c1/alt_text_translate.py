import os
from google.cloud import translate_v2 as translate


def translate_alt_text(text: str, target_language: str = "es") -> str:
    """
    Translates generated image descriptions using Google Cloud Translation.
    Relies on GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    client = translate.Client()

    # Text can also be a list of strings, in which case a list of translations is returned.
    result = client.translate(text, target_language=target_language)

    return result["translatedText"]
