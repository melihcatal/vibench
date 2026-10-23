import os
from google.cloud import translate_v2 as translate


def translate_query(query: str, target_language: str) -> str:
    """
    Translates a query before multilingual embedding search using Google Cloud Translate.
    """
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise EnvironmentError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable not set."
        )

    translate_client = translate.Client()

    result = translate_client.translate(query, target_language=target_language)

    return result["translatedText"]
