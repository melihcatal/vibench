from typing import Dict, List
import requests
from document_models import OCRResponse


def ocr_translate(text: str, target_language: str = "es") -> str:
    """Translate extracted OCR text using DeepL API."""
    api_key = "DEEPL_API_KEY"  # Replace with environment variable in production
    url = "https://api-free.deepl.com/v2/translate"

    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/json",
    }

    data = {"text": [text], "target_lang": target_language}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()["translations"][0]["text"]
