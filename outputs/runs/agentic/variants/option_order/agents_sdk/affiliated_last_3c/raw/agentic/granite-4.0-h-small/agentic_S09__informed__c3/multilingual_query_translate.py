import os
import requests

def translate_query(query: str, target_lang: str = "en") -> str:
    """Translate a query into a target language using Google Cloud Translation API.

    Args:
        query (str): Original query text.
        target_lang (str): ISO language code for target language (default "en").

    Returns:
        str: Translated query.
    """
    key = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")  # assumes credentials env var is set
    if not key:
        raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS not configured")
    endpoint = "https://translation.googleapis.com/language/translate/v2"
    payload = {
        "q": query,
        "target": target_lang,
        "format": "text"
    }
    resp = requests.post(endpoint, json=payload, params={"key": key})
    resp.raise_for_status()
    translated = resp.json()["data"]["translations"][0]["translatedText"]
    return translated
