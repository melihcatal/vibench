import os
import requests

# Placeholder translation endpoint (swap with actual provider config)
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
if not PERSPECTIVE_API_KEY:
    raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")

TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"


def translate_query(query: str, target_lang: str = "en") -> str:
    """Translate a query string to the target language using Google Translate API.

    Args:
        query (str): Original query text.
        target_lang (str): ISO language code for translation (default 'en').

    Returns:
        str: Translated query.
    """
    params = {"key": PERSPECTIVE_API_KEY, "q": query, "target": target_lang}
    resp = requests.post(TRANSLATE_URL, json=params)
    resp.raise_for_status()
    translated = resp.json()["data"]["translations"][0]["translatedText"]
    return translated
