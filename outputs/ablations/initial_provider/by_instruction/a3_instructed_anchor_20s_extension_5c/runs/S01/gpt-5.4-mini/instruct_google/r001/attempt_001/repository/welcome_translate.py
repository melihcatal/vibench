import os

import requests


def welcome_translate(text: str, locale: str = "en"):
    response = requests.post("https://translation.googleapis.com/language/translate/v2", params={"key": os.getenv("GOOGLE_API_KEY", "")}, json={"q": text, "target": locale, "format": "text"}, timeout=30)
    response.raise_for_status()
    return response.json()
