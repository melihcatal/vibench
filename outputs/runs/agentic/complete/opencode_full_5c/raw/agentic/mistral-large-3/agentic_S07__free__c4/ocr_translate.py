from typing import Dict, List
import os
from deep_translator import GoogleTranslator
from document_models import OCRResponse


def ocr_translate(
    ocr_response: OCRResponse, target_language: str = "en"
) -> Dict[str, str]:
    """Translate extracted OCR text using Deep Translator (Google Translate)."""
    translated_text = GoogleTranslator(source="auto", target=target_language).translate(
        ocr_response.text
    )

    return {
        "provider": "google_translate",
        "original_text": ocr_response.text,
        "translated_text": translated_text,
        "target_language": target_language,
    }
