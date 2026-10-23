"""
Translate extracted OCR text using the DeepL Translation API.
Uses the official DeepL Python SDK for text translation of OCR results.
"""

import os
from typing import List, Optional

import deepl

from document_models import DocumentTextResult


def get_deepl_auth_key() -> str:
    """Retrieve DeepL authentication key from environment."""
    key = os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    return key


def create_deepl_translator() -> deepl.Translator:
    """
    Create and return a DeepL Translator client.

    Returns:
        deepl.Translator: Authenticated DeepL translator client.
    """
    auth_key = get_deepl_auth_key()
    return deepl.Translator(auth_key)


def translate_ocr_text(
    ocr_result: DocumentTextResult,
    target_language: str = "EN-US",
    source_language: Optional[str] = None,
) -> DocumentTextResult:
    """
    Translate the full text and individual blocks from OCR result using DeepL API.

    Args:
        ocr_result: The DocumentTextResult from OCR extraction.
        target_language: Target language code (e.g., 'EN-US', 'DE', 'FR', 'ES').
        source_language: Optional source language code. If None, DeepL auto-detects.

    Returns:
        DocumentTextResult: New result with translated text content.
    """
    translator = create_deepl_translator()

    # Translate full text
    full_translation = translator.translate_text(
        ocr_result.full_text,
        target_lang=target_language,
        source_lang=source_language,
    )
    translated_full_text = full_translation.text

    # Translate individual blocks
    translated_blocks = []
    for block in ocr_result.blocks:
        if block.content.strip():
            block_translation = translator.translate_text(
                block.content,
                target_lang=target_language,
                source_lang=source_language,
            )
            translated_blocks.append(
                type(block)(
                    content=block_translation.text,
                    confidence=block.confidence,
                    bounding_box=block.bounding_box,
                    page_number=block.page_number,
                )
            )
        else:
            translated_blocks.append(block)

    return DocumentTextResult(
        full_text=translated_full_text,
        blocks=translated_blocks,
        page_count=ocr_result.page_count,
    )


def translate_text_string(
    text: str,
    target_language: str = "EN-US",
    source_language: Optional[str] = None,
) -> str:
    """
    Translate a plain text string using DeepL API.

    Args:
        text: The text to translate.
        target_language: Target language code.
        source_language: Optional source language code for auto-detection.

    Returns:
        str: Translated text string.
    """
    translator = create_deepl_translator()
    result = translator.translate_text(
        text,
        target_lang=target_language,
        source_lang=source_language,
    )
    return result.text


def translate_batch(
    texts: List[str],
    target_language: str = "EN-US",
    source_language: Optional[str] = None,
) -> List[str]:
    """
    Translate a batch of text strings using DeepL API.

    Args:
        texts: List of text strings to translate.
        target_language: Target language code.
        source_language: Optional source language code.

    Returns:
        List[str]: List of translated text strings.
    """
    translator = create_deepl_translator()
    results = translator.translate_text(
        texts,
        target_lang=target_language,
        source_lang=source_language,
    )
    return [r.text for r in results]
