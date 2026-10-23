from typing import Dict
import requests
import os


def translate_appeal_text(text: str, target_language: str = "en") -> str:
    """
    Translates appeal text for review using DeepL API.
    API: https://api-free.deepl.com/v2/translate
    Model: DeepL-Pro
    """
    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        data={
            "auth_key": os.getenv("DEEPL_API_KEY"),
            "text": text,
            "target_lang": target_language,
        },
    )
    response.raise_for_status()
    return response.json()["translations"][0]["text"]
