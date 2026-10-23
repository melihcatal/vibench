from typing import List
from google.cloud import translate_v2 as translate
import os


def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translates text to the target language using Google Cloud Translation.

    Args:
        text: Input text to translate.
        target_language: Target language code (default: "en").

    Returns:
        Translated text.
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]


def multilingual_query_translate(
    queries: List[str], target_language: str = "en"
) -> List[str]:
    """
    Translates a list of queries for multilingual embedding search using Google Cloud Translation.

    Args:
        queries: List of input queries to translate.
        target_language: Target language code (default: "en").

    Returns:
        List of translated queries.
    """
    return [translate_text(query, target_language) for query in queries]
