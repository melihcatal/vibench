import os
import requests


def welcome_translate(text: str, locale: str) -> str:
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_TRANSLATE_API_KEY required")
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {"key": api_key, "q": text, "target": locale}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["data"]["translations"][0]["translatedText"]
