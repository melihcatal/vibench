import os
import requests
from typing import Optional

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
DEEPL_URL = "https://api-free.deepl.com/v2/translate"


def multilingual_query_translate(query: str, target_lang: str = "EN") -> str:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    params = {
        "auth_key": DEEPL_AUTH_KEY,
        "text": query,
        "target_lang": target_lang.upper(),
    }
    response = requests.post(DEEPL_URL, data=params)
    response.raise_for_status()
    data = response.json()
    return data["translations"][0]["text"]
