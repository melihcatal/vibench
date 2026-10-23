"""
[LATER-STEP] Translate extracted OCR text using Google Cloud Translation API.
Translates document text extracted by OCR into target languages using
Google Cloud Translation v2 with the nmt (neural machine translation) model.
"""

import os
from typing import Optional, List
from google.cloud import translate_v2 as translate

from document_client import GOOGLE_CLOUD_PROJECT


GOOGLE_CLOUD_TRANSLATION_MODEL = "nmt"
GOOGLE_CLOUD_TRANSLATION_ENDPOINT = "translation.googleapis.com"


class GoogleTranslationClient:
    """Client wrapper for Google Cloud Translation API."""

    def __init__(
        self,
        project: Optional[str] = None,
        credentials_path: Optional[str] = None,
    ):
        self.project = project or GOOGLE_CLOUD_PROJECT
        self.client = translate.Client()

    def translate_text(
        self,
        text: str,
        target_language: str = "en",
        source_language: Optional[str] = None,
        model: str = GOOGLE_CLOUD_TRANSLATION_MODEL,
        format_type: str = "text",
    ) -> dict:
        """
        Translate text using Google Cloud Translation API.

        Uses the nmt (neural machine translation) model for high-quality translation.

        Args:
            text: The text to translate.
            target_language: Target language code (e.g., "en", "es", "fr").
            source_language: Optional source language code for auto-detection.
            model: Translation model - "nmt" for neural machine translation.
            format_type: Input format - "text" or "html".

        Returns:
            Dictionary with translated text and metadata.
        """
        kwargs = {
            "target_language": target_language,
            "format_": format_type,
            "model": model,
        }

        if source_language:
            kwargs["source_language"] = source_language

        result = self.client.translate(text, **kwargs)
        return result

    def translate_batch(
        self,
        texts: List[str],
        target_language: str = "en",
        source_language: Optional[str] = None,
        model: str = GOOGLE_CLOUD_TRANSLATION_MODEL,
    ) -> List[dict]:
        """Translate a batch of texts."""
        results = []
        for text in texts:
            result = self.translate_text(
                text, target_language, source_language, model
            )
            results.append(result)
        return results


def translate_ocr_text(
    ocr_text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    client: Optional[GoogleTranslationClient] = None,
) -> dict:
    """
    Translate OCR-extracted text using Google Cloud Translation API.

    Uses the nmt model (neural machine translation) via translation.googleapis.com
    for accurate translation of scanned document content.

    Args:
        ocr_text: Plain text extracted from OCR.
        target_language: Target language code (e.g., "en", "es", "fr", "de", "ja").
        source_language: Optional source language (auto-detected if not provided).
        client: Optional pre-configured GoogleTranslationClient.

    Returns:
        Dictionary containing translated text, detected source language, and confidence.
    """
    if client is None:
        client = GoogleTranslationClient()

    if not ocr_text.strip():
        return {
            "original_text": "",
            "translated_text": "",
            "detected_source_language": "",
            "model": GOOGLE_CLOUD_TRANSLATION_MODEL,
        }

    result = client.translate_text(
        text=ocr_text,
        target_language=target_language,
        source_language=source_language,
        model=GOOGLE_CLOUD_TRANSLATION_MODEL,
    )

    return {
        "original_text": ocr_text,
        "translated_text": result.get("translatedText", ""),
        "detected_source_language": result.get("detectedSourceLanguage", source_language or "auto"),
        "model": GOOGLE_CLOUD_TRANSLATION_MODEL,
    }


def translate_ocr_blocks(
    blocks: list,
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> list:
    """
    Translate individual OCR text blocks while preserving structure.

    Args:
        blocks: List of text block objects with .text attribute.
        target_language: Target language code.
        source_language: Optional source language code.

    Returns:
        List of dictionaries with original and translated text for each block.
    """
    client = GoogleTranslationClient()
    results = []

    for block in blocks:
        text = getattr(block, 'text', '') if hasattr(block, 'text') else block.get('text', '')
        if not text.strip():
            continue

        translation = client.translate_text(
            text=text,
            target_language=target_language,
            source_language=source_language,
            model=GOOGLE_CLOUD_TRANSLATION_MODEL,
        )

        results.append({
            "original_text": text,
            "translated_text": translation.get("translatedText", ""),
            "detected_language": translation.get("detectedSourceLanguage", ""),
        })

    return results


def detect_language(text: str) -> dict:
    """
    Detect the language of OCR text using Google Cloud Translation API.

    Args:
        text: The text to analyze.

    Returns:
        Dictionary with detected language, confidence, and reliability.
    """
    client = GoogleTranslationClient()
    detections = client.client.detect_language(text)

    if isinstance(detections, dict):
        return {
            "language": detections.get("language", ""),
            "confidence": detections.get("confidence", 0.0),
            "is_reliable": detections.get("isReliable", False),
        }

    return {
        "language": "",
        "confidence": 0.0,
        "is_reliable": False,
    }


if __name__ == "__main__":
    sample_ocr = """Invoice #12345
Date: 2024-01-15
Total: $150.00
Description: Professional services rendered"""

    result = translate_ocr_text(sample_ocr, target_language="es")
    print(f"Translated ({result['detected_source_language']} -> es):")
    print(result["translated_text"])
