import os
import requests
from typing import Dict, Any

# Google Cloud Translation endpoint (replace with real if needed)
TRANSLATE_API_URL = "https://translation.googleapis.com/language/translate/v2"
TRANSLATE_API_KEY = os.getenv("GOOGLE_API_KEY")


def translate_text(text: str, target_lang: str = "es") -> Dict[str, Any]:
    """Translate text using Google Cloud Translation API."""
    params = {
        "q": text,
        "target": target_lang,
        "format": "text",
        "key": TRANSLATE_API_KEY,
    }
    response = requests.get(TRANSLATE_API_URL, params=params)
    response.raise_for_status()
    return response.json()


def extract_translated_text(json_resp: Dict[str, Any]) -> str:
    """Extract the first translated segment from the API response."""
    data = json_resp.get("data", {})
    translations = data.get("translations", [])
    if not translations:
        raise ValueError("No translations returned")
    return translations[0].get("translatedText", "")
