import os
from google.cloud import translate_v2 as translate


def translate_script(text: str, target_language_code: str) -> str:
    """
    Translates narration scripts using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language_code)
    return result["translatedText"]
