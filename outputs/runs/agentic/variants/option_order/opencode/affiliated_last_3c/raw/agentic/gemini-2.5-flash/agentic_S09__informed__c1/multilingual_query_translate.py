import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any


def translate_query(
    query: str, target_language: str, source_language: str = None
) -> Dict[str, Any]:
    """
    Translates a query using Google Cloud Translation.
    """
    # Google Cloud Translation client will use GOOGLE_APPLICATION_CREDENTIALS
    # environment variable for authentication.
    client = translate.Client()

    result = client.translate(
        query, target_language=target_language, source_language=source_language
    )
    return result
