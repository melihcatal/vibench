import os
from google.cloud import translate_v2 as translate


def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translates text into the target language using Google Cloud Translation API.
    """
    # Provider-specific client class from the google-cloud-translate SDK
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Provider-specific API method
    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
