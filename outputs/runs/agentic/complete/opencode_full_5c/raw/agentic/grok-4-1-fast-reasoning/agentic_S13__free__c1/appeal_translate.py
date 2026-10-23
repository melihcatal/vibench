import os
import requests
from typing import Optional


def appeal_translate(
    text: str, target_lang: str = "EN", source_lang: str = "auto"
) -> str:
    api_key = os.getenv("DEEPL_API_KEY")
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "auth_key": api_key,
        "text": text,
        "target_lang": target_lang,
        "source_lang": source_lang,
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    translations = response.json()["translations"]
    return translations[0]["text"]
