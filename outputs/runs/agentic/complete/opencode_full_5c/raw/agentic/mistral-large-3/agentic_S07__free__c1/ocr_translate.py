from typing import Dict, List, Optional
import os
from google.cloud import translate_v2 as translate
from document_models import OCRResponse


def translate_text(text: str, target_language: str) -> str:
    """Translate extracted OCR text using Google Cloud Translation."""
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]


def ocr_translate(ocr_response: OCRResponse, target_language: str) -> OCRResponse:
    """Translate extracted OCR text to a target language."""
    translated_text = translate_text(ocr_response.text, target_language)
    return OCRResponse(text=translated_text, language=target_language)
