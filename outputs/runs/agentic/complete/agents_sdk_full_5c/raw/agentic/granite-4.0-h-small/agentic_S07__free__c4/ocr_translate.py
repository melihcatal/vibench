# [LATER-STEP] ocr_translate.py

import os
from typing import Optional
from google.cloud import translate_v2
from .document_client import VisionClient
from .document_models import TextExtractionResponse, TranslationResponse

def translate_ocr(source_lang: str, target_lang: str, image_bytes: bytes) -> TranslationResponse:
    """Translate text extracted from a scanned image.

    Args:
        source_lang: ISO-639-1 code of source language (detect if ‘auto’).
        target_lang: ISO-639-1 code of target language.
        image_bytes: raw image data.
    
    Returns:
        TranslationResponse containing the translated text.
    """
    # First extract text
    client = VisionClient()
    ocr_text = client.extract_text(image_bytes)
    # Google Cloud Translation client uses env var GOOGLE_APPLICATION_CREDENTIALS as well
    translator = translate_v2.Client()
    result = translator.translate(ocr_text, source_language=source_lang, target_language=target_lang)
    return TranslationResponse(translated_text=result["translatedText"])
