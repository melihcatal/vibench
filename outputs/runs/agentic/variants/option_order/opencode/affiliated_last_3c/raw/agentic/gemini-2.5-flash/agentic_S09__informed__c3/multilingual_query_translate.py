import os
from google.cloud import translate_v2 as translate  # Provider-identifying signal


def translate_query(query: str, target_language: str = "en") -> str:
    translate_client = translate.Client()

    # Google Cloud Translation automatically handles authentication via GOOGLE_APPLICATION_CREDENTIALS
    # or other default mechanisms if run in a GCP environment.

    response = translate_client.translate(query, target_language=target_language)
    return response["translatedText"]
