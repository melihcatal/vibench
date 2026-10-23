import os
from typing import Dict, Any
import requests
from document_models import TranslationResponse


def translate_text(text: str, target_language: str = "es") -> TranslationResponse:
    """
    Translate extracted OCR text using Google Cloud Translation API.
    """
    api_key = os.getenv("GOOGLE_CLOUD_TRANSLATE_API_KEY")
    
    # Google Cloud Translation API-specific request
    request_payload = {
        "q": text,
        "target": target_language,
        "format": "text"
    }
    
    response = requests.post(
        f"https://translation.googleapis.com/language/translate/v2?key={api_key}",
        json=request_payload
    )
    response.raise_for_status()
    
    result = response.json()
    translated_text = result.get("data", {}).get("translations", [{}])[0].get("translatedText", "")
    source_language = result.get("data", {}).get("translations", [{}])[0].get("detectedSourceLanguage", "")
    
    return TranslationResponse(
        translated_text=translated_text,
        source_language=source_language,
        target_language=target_language,
        provider="google_cloud_translation",
        raw_response=result
    )