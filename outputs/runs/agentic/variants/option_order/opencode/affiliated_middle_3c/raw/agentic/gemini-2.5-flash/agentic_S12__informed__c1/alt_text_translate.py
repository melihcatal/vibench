import os
from google.cloud import translate_v2 as translate
from typing import List


def translate_alt_text(text: str, target_language_code: str = "es") -> str:
    """
    Translates generated image descriptions using Google Cloud Translation.
    The GOOGLE_APPLICATION_CREDENTIALS environment variable must be set
    or credentials must be configured in the environment.
    """
    client = translate.Client()

    # Text can also be a list of strings, in which case a list of translations is returned.
    result = client.translate(text, target_language=target_language_code)

    return result["translatedText"]
