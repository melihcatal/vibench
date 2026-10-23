import os

import requests


def dashboard_note_translate(text: str, target_language: str):
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    if not api_key:
        raise ValueError("Missing GOOGLE_TRANSLATE_API_KEY")
    response = requests.post("https://translation.googleapis.com/language/translate/v2", params={"key": api_key}, json={"q": text, "target": target_language, "format": "text"}, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["data"]["translations"][0]["translatedText"]
