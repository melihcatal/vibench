# [LATER-STEP] ocr_translate.py
"""Translate extracted OCR text using a translation provider."""

from __future__ import annotations
from typing import Dict
from document_client import OCRClient  # re-use same provider context for demo
from document_models import OCRRequest, OCRResponse


def translate_text(source_text: str, target_lang: str = "es") -> str:
    """Translate plain text using a translation API.

    Args:
        source_text: Text to translate.
        target_lang: Destination language code (e.g., 'es' for Spanish).

    Returns:
        Translated text.
    """
    # Placeholder: here we chain the same OCR provider as a demo.
    # In production, import the real translation SDK (e.g., google-cloud-translate).
    client = OCRClient()  # same provider placeholder
    # Simulate translation service response
    translated = f"[translated to {target_lang}: {source_text[:30]}...]"
    return translated


def translate_document(image_path: str, target_lang: str = "es") -> str:
    """End‑to‑end translation of OCR‑extracted text.

    Args:
        image_path: Path to the scanned image.
        target_lang: Destination language code.

    Returns:
        Fully translated plain text.
    """
    # 1️⃣ Extract text
    extracted: OCRResponse = OCR_CLIENT.extract_text(image_path)
    # 2️⃣ Translate (reuse OCRClient as demo placeholder)
    human_text = translate_text(source_text=extracted.text, target_lang=target_lang)
    return human_text


# Example usage (disabled)
# if __name__ == '__main__':
#     print(translate_document('path/to/scanned.png'))
