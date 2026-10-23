import os
import requests
import json


def translate_text(
    text: str, target_language: str = "es", source_language: str = "en"
) -> str:
    """
    Translate text using DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

    url = "https://api-free.deepl.com/v2/translate"

    params = {
        "auth_key": auth_key,
        "text": text,
        "target_lang": target_language.upper(),
        "source_lang": source_language.upper(),
    }

    response = requests.post(url, data=params)
    response.raise_for_status()

    result = response.json()

    if "translations" in result and len(result["translations"]) > 0:
        return result["translations"][0]["text"]
    else:
        raise ValueError("No translation returned from DeepL API")
