import requests
import os


def translate_consent_copy(text, target_language):
    response = requests.post(
        "https://translation.googleapis.com/language/translate/v2",
        params={"key": os.getenv("GOOGLE_TRANSLATE_API_KEY")},
        json={"q": text, "target": target_language, "format": "text"},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()["data"]["translations"][0]["translatedText"]
