import os
from typing import Dict, Any
import requests
from document_models import TranslationResponse


def translate_text(text: str, target_language: str) -> TranslationResponse:
    """
    Translate extracted OCR text using DeepL API.
    """
    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        data={
            "auth_key": os.getenv("DEEPL_API_KEY"),
            "text": text,
            "target_lang": target_language
        }
    )
    
    response.raise_for_status()
    result = response.json()
    
    return TranslationResponse(
        translated_text=result["translations"][0]["text"],
        source_language=result["translations"][0]["detected_source_language"],
        target_language=target_language,
        provider="deepl"
    )