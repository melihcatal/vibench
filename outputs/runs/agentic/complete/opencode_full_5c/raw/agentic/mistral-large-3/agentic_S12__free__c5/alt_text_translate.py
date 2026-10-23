from typing import Optional
import requests


def translate_text(text: str, target_language: str = "es") -> Optional[str]:
    """Translates text using Google Cloud Translation API."""
    api_key = (
        "YOUR_GOOGLE_CLOUD_API_KEY"  # Replace with environment variable in production
    )
    url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"

    payload = {"q": text, "target": target_language}

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Google Cloud Translation API error: {response.text}")

    translated_text = (
        response.json()
        .get("data", {})
        .get("translations", [{}])[0]
        .get("translatedText", None)
    )
    return translated_text
