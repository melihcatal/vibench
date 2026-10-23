import os
from google.cloud import (
    translate_v2 as translate,
)  # example provider; replace as needed


def translate_query(query: str, target_lang: str = "en") -> str:
    """
    Translate a query string into the target language using a translation service.

    Args:
        query (str): Original query text.
        target_lang (str): ISO language code to translate to (default 'en').

    Returns:
        str: Translated query.
    """
    api_key = os.getenv(
        "GOOGLE_API_KEY"
    )  # replace with appropriate env var for other providers
    if not api_key:
        raise RuntimeError("Missing GOOGLE_API_KEY environment variable")
    client = translate.Client(api_key=api_key)
    result = client.translate(query, target_language=target_lang)
    return result["translatedText"]
