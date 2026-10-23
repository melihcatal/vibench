import os
import requests
import google.cloud.translate_v2 as translate

# Identifier: Google Cloud Translation SDK

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS env variable")

translate_client = translate.Client()


def multilingual_query_translate(query: str, target_lang: str = "en") -> str:
    """Translate a query into the target language using Google Cloud Translation.

    Args:
        query: Original query text.
        target_lang: ISO language code to translate to (default English).

    Returns:
        Translated query string.
    """
    result = translate_client.translate(query, target_language=target_lang)
    return result["translatedText"]
