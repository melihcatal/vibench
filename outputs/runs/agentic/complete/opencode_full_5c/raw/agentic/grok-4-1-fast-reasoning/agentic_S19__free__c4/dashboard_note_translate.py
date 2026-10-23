import os
import requests
from typing import Any


def translate_dashboard_note(
    text: str, target_lang: str = "FR", source_lang: str = "EN"
) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set.")
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "auth_key": auth_key,
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang,
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    translations = response.json()["translations"]
    return translations[0]["text"]
