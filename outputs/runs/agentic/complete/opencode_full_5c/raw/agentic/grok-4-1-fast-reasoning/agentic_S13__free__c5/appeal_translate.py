import os
import requests
from typing import Any

TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"


def appeal_translate(text: str, target_language: str = "es") -> str:
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    params = {"key": api_key, "q": text, "target": target_language}
    response = requests.get(TRANSLATE_URL, params=params)
    response.raise_for_status()
    data = response.json()["data"]["translations"][0]
    return data["translatedText"]
