from typing import Dict, List
import requests
from document_models import OCRResponse


def translate_text(text: str, target_language: str) -> str:
    """Translate extracted OCR text using DeepL API."""
    deepl_api_key = "DEEPL_API_KEY"  # Replace with environment variable in production
    url = "https://api-free.deepl.com/v2/translate"

    headers = {
        "Authorization": f"DeepL-Auth-Key {deepl_api_key}",
        "Content-Type": "application/json",
    }

    data = {"text": [text], "target_lang": target_language}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()["translations"][0]["text"]


def ocr_translate(ocr_response: OCRResponse, target_language: str) -> Dict[str, str]:
    """Translate extracted OCR text from a document."""
    translated_text = translate_text(ocr_response.full_text, target_language)

    return {
        "original_text": ocr_response.full_text,
        "translated_text": translated_text,
        "provider": "deepl",
        "model": "deepl_free",
        "target_language": target_language,
    }
