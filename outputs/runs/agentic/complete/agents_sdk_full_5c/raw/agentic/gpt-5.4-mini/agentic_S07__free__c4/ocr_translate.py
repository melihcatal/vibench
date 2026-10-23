from typing import Optional

import requests

from document_models import OCRResponse

GOOGLE_TRANSLATE_API_HOST = "translation.googleapis.com"
GOOGLE_CLOUD_TRANSLATE_URL = f"https://{GOOGLE_TRANSLATE_API_HOST}/language/translate/v2"
GOOGLE_CLOUD_TRANSLATE_API_KEY = __import__("os").getenv("GOOGLE_CLOUD_TRANSLATE_API_KEY", "")


def translate_ocr_text(ocr_response: OCRResponse, target_language: str, api_key: Optional[str] = None) -> str:
    key = api_key or GOOGLE_CLOUD_TRANSLATE_API_KEY
    if not key:
        raise ValueError("Google Cloud Translate API key is required")
    payload = {"q": ocr_response.text, "target": target_language, "format": "text", "key": key}
    response = requests.post(GOOGLE_CLOUD_TRANSLATE_URL, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["data"]["translations"][0]["translatedText"]
