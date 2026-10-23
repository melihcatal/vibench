from typing import Dict
import requests


def translate_appeal_text(text: str, target_language: str = "en") -> str:
    api_key = "YOUR_DEEPL_API_KEY"  # Replace with environment variable in production
    url = "https://api-free.deepl.com/v2/translate"

    data = {"auth_key": api_key, "text": text, "target_lang": target_language}

    response = requests.post(url, data=data)
    response.raise_for_status()

    return response.json()["translations"][0]["text"]
