import os
from google.cloud import translate_v2 as translate


def multilingual_query_translate(query: str, target_language: str = "en") -> str:
    """
    Translate queries before multilingual embedding search using Google Cloud Translate.
    """
    os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    translate_client = translate.Client()

    result = translate_client.translate(query, target_language=target_language)

    return result["translatedText"]
