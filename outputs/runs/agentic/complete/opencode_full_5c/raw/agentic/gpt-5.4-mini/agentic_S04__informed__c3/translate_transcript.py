import requests

from speech_client import get_base_url, get_headers


def translate_transcript(text: str, target_language: str = "en"):
    response = requests.post(
        "https://translation.googleapis.com/language/translate/v2",
        headers={"content-type": "application/json"},
        params={"key": __import__("os").getenv("GOOGLE_TRANSLATE_API_KEY", "")},
        json={"q": text, "target": target_language, "format": "text"},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
