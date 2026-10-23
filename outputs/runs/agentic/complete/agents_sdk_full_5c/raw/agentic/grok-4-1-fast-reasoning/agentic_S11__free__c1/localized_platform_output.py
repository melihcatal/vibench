import os
from google.cloud import translate_v2 as translate

def localized_platform_output(text: str, target_language: str = "fr") -> str:
    """
    Translate platform output using Google Cloud Translation API.
    """
    client = translate.Client()
    result = client.translate(
        text,
        target_language=target_language
    )
    return result["translatedText"]
