import os
import requests
from typing import Optional

def translate_query(query: str, target_lang: str = "EN", source_lang: str = "auto") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "auth_key": auth_key,
        "text": query,
        "source_lang": source_lang,
        "target_lang": target_lang
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    translations = response.json()["translations"]
    return translations[0]["text"]