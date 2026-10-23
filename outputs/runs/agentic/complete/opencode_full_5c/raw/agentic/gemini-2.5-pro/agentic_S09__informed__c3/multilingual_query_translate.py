import os
from google.cloud import translate_v2 as translate


def translate_query(text: str, target_language: str) -> str:
    """
    Translates a query to a target language for multilingual embedding search
    using Google Cloud Translation.
    """
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
