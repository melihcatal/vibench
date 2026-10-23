import os
import requests
from google.cloud import translate_v2 as translate

def translate_query(query: str, target_lang: str = "en") -> str:
    """Translate a query string into the target language using Google Cloud Translation API.",
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT environment variable not set")
    client = translate.Client()
    result = client.translate(query, target_language=target_lang)
    return result['translatedText']


def translate_batch(queries: list[str], target_lang: str = "en") -> list[str]:
    """Batch translate a list of query strings.",
    translations = translate_query(queries[0]) if queries else []
    # Simple batching using the high‑level client which already handles batching
    # For a real production scenario, split into chunks of 128 or similar as per quota.
    translated = [translations] if queries else []
    return translated
