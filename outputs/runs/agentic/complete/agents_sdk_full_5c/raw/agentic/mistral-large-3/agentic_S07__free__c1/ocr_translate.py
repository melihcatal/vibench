import os
from typing import Optional
from google.cloud import translate_v2 as translate
from document_models import OCRTextResponse

def translate_text(text_response: OCRTextResponse, target_language: str) -> OCRTextResponse:
    """Translate extracted OCR text using Google Cloud Translation."""
    client = translate.Client()
    result = client.translate(text_response.text, target_language=target_language)
    
    return OCRTextResponse(
        text=result['translatedText'],
        language=target_language
    )