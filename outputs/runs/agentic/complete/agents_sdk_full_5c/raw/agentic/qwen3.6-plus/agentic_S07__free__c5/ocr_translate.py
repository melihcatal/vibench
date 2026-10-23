"""
Translate extracted OCR text using Google Cloud Translation API.

Uses the Google Cloud Translation v2 API to translate text extracted
from OCR operations into a target language.
"""

import os
from typing import Optional, List

from google.cloud import translate_v2 as translate


# Google Cloud Translation API configuration
GOOGLE_TRANSLATE_API_HOST = "translation.googleapis.com"
GOOGLE_TRANSLATE_MODEL = "nmt"  # Neural Machine Translation model


def translate_ocr_text(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    format_type: str = "text",
) -> str:
    """
    Translate extracted OCR text using Google Cloud Translation API.
    
    This function uses the Google Cloud Translation v2 API with the
    Neural Machine Translation (NMT) model to translate text extracted
    from OCR operations.
    
    Args:
        text: The OCR-extracted text to translate.
        target_language: Target language code (e.g., 'en', 'es', 'fr').
        source_language: Source language code (auto-detect if None).
        format_type: Format of the text ('text' or 'html').
        
    Returns:
        str: Translated text.
        
    Raises:
        ValueError: If text is empty.
        Exception: If Google Translation API call fails.
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    client = translate.Client()
    
    translate_kwargs = {
        "target": target_language,
        "format_": format_type,
        "model": GOOGLE_TRANSLATE_MODEL,
    }
    
    if source_language:
        translate_kwargs["source_language"] = source_language
    
    result = client.translate(text, **translate_kwargs)
    return result["translatedText"]


def translate_ocr_text_batch(
    texts: List[str],
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> List[str]:
    """
    Translate a batch of OCR-extracted text segments.
    
    Args:
        texts: List of text segments to translate.
        target_language: Target language code.
        source_language: Source language code (auto-detect if None).
        
    Returns:
        List[str]: List of translated texts.
    """
    if not texts:
        return []
    
    client = translate.Client()
    
    translate_kwargs = {
        "target": target_language,
        "model": GOOGLE_TRANSLATE_MODEL,
    }
    
    if source_language:
        translate_kwargs["source_language"] = source_language
    
    results = client.translate(texts, **translate_kwargs)
    
    if isinstance(results, dict):
        return [results["translatedText"]]
    
    return [r["translatedText"] for r in results]


def translate_with_detection(
    text: str,
    target_language: str = "en",
) -> dict:
    """
    Translate OCR text and detect the source language.
    
    Args:
        text: The OCR-extracted text to translate.
        target_language: Target language code.
        
    Returns:
        dict: Dictionary with translated text, detected source language, and confidence.
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    client = translate.Client()
    
    result = client.translate(
        text,
        target=target_language,
        model=GOOGLE_TRANSLATE_MODEL,
    )
    
    return {
        "translated_text": result["translatedText"],
        "detected_source": result.get("detectedSourceLanguage", "unknown"),
        "confidence": result.get("confidence", 0.0),
    }


def get_supported_languages() -> List[dict]:
    """
    Get list of supported languages from Google Cloud Translation API.
    
    Returns:
        List[dict]: List of supported languages with codes and names.
    """
    client = translate.Client()
    languages = client.get_languages()
    return languages
