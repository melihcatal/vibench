import os
from google.cloud import translate_v2 as translate

def translate_query(query: str, target_language: str = "en") -> str:
    """
    Translates a query into the target language using Google Cloud Translate API.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.

    Args:
        query: The text query to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'en').

    Returns:
        The translated query string.
    """
    # The client automatically uses credentials from the environment.
    translate_client = translate.Client()

    if isinstance(query, bytes):
        query = query.decode("utf-8")

    result = translate_client.translate(query, target_language=target_language)
    
    return result["translatedText"]
