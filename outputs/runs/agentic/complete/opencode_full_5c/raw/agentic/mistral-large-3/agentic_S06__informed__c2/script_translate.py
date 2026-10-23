from typing import Dict, Any
import os
import requests


def translate_text(
    text: str, target_language: str, source_language: str = "auto"
) -> str:
    """
    Translates narration scripts using DeepL API before synthesis.
    """
    api_key = os.getenv("DEEPL_AUTH_KEY")
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": api_key,
        "text": text,
        "target_lang": target_language,
        "source_lang": source_language,
    }
    response = requests.post(url, data=params)
    response.raise_for_status()
    return response.json()["translations"][0]["text"]
