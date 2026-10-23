import os
from typing import Dict
from google.cloud import translate_v2 as translate
from document_models import TextExtractionResponse

def translate_text(text_response: TextExtractionResponse, target_language: str) -> Dict[str, str]:
    """Translate extracted OCR text using Google Cloud Translation."""
    client = translate.Client()
    
    if isinstance(text_response.full_text, bytes):
        text = text_response.full_text.decode("utf-8")
    else:
        text = text_response.full_text
    
    result = client.translate(text, target_language=target_language)
    
    return {
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
        "provider": "google_cloud_translation",
        "model": "base"
    }