import os
import requests
from typing import Optional

GOOGLE_TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"


def appeal_translate(appeal_text: str, target_language: str = "en") -> str:
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    if not api_key:
        raise ValueError("Google Translate API key not configured")
    params = {
        "key": api_key,
        "q": appeal_text,
        "target": target_language,
        "format": "text",
    }
    response = requests.get(GOOGLE_TRANSLATE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data["data"]["translations"][0]["translatedText"]
