from typing import Dict, Optional
import os
from google.cloud import translate_v2 as translate
from document_client import get_document_client
from document_models import OCRResponse


def translate_text(text: str, target_language: str = "en") -> str:
    """Translate extracted OCR text using Google Cloud Translation."""
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]


def ocr_translate(image_path: str, target_language: str = "en") -> str:
    """Extract text from an image and translate it using Google Cloud Translation."""
    from extract_text import extract_text

    ocr_result = extract_text(image_path)
    translated_text = translate_text(ocr_result.text, target_language)
    return translated_text
