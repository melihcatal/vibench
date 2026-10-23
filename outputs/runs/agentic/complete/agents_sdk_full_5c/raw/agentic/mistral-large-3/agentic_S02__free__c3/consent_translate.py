import os
import requests
from typing import Dict


def translate_consent_text(text: str, target_language: str) -> str:
    # Using Google Cloud Translation API
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    
    url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"
    payload = {
        "q": text,
        "target": target_language,
        "format": "text",
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    translated_text = response.json()["data"]["translations"][0]["translatedText"]
    return translated_text