import os
from google.cloud import translate_v2 as translate

def translate_script(text: str, target_language: str = "en") -> str:
    """
    Translates narration scripts using Google Cloud Translation API.
    """
    client = translate.Client()

    # Text can also be a list of strings, in which case a list of translations is returned.
    result = client.translate(text, target_language=target_language)

    return result["translatedText"]
