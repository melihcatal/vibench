import os
from google.cloud import translate_v2 as translate
from typing import List


def translate_query(query: str, target_language: str = "en") -> str:
    """Translates a query to a target language using Google Cloud Translation."""
    # Google Cloud Translation typically uses GOOGLE_APPLICATION_CREDENTIALS for authentication.
    # Ensure your environment is set up with these credentials.
    # For this example, we assume the credentials are implicitly available or configured.
    # If using API Key directly, client initialization would differ.

    translate_client = translate.Client()

    # Target can be a language code, e.g. "en"
    result = translate_client.translate(query, target_language=target_language)

    # The translated text is in result['translatedText']
    return result["translatedText"]
