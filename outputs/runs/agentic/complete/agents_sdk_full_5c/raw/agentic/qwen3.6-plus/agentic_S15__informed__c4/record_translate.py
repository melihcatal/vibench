"""
Translate user-facing document fields using Google Cloud Translation API.

Provider: Google Cloud Translation
SDK: google-cloud-translate
Auth: GOOGLE_APPLICATION_CREDENTIALS
Interface: SDK
"""

import os
from typing import Any, Dict, List, Optional

from google.cloud import translate_v2 as translate


def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    format_type: str = "text",
) -> Dict[str, Any]:
    """
    Translate a single text string using the Google Cloud Translation v2 API.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., 'en', 'fr', 'ja').
        source_language: Optional source language code; auto-detected if None.
        format_type: Input format, 'text' or 'html'.

    Returns:
        A dict with translated text, detected source language, and metadata.
    """
    client = translate.Client()

    kwargs: Dict[str, Any] = {
        "target_language": target_language,
        "format_": format_type,
    }

    if source_language:
        kwargs["source_language"] = source_language

    result = client.translate(text, **kwargs)

    return {
        "translated_text": result.get("translatedText", ""),
        "detected_source_language": result.get("detectedSourceLanguage", source_language or "unknown"),
        "target_language": target_language,
        "input_text": text,
    }


def translate_document_fields(
    document: Dict[str, Any],
    text_fields: Optional[List[str]] = None,
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate specified text fields within a document using Google Cloud Translation.

    Args:
        document: The document containing fields to translate.
        text_fields: List of field names to translate. Defaults to common text fields.
        target_language: The target language code.
        source_language: Optional source language; auto-detected if None.

    Returns:
        A dict with translated document, per-field translation results, and metadata.
    """
    if text_fields is None:
        text_fields = ["title", "content", "description", "body", "summary", "notes"]

    translated_document = dict(document)
    field_results = {}
    translation_count = 0

    for field_name in text_fields:
        field_value = document.get(field_name)
        if field_value is not None and isinstance(field_value, str):
            translation_result = translate_text(
                text=field_value,
                target_language=target_language,
                source_language=source_language,
            )
            translated_document[field_name] = translation_result["translated_text"]
            field_results[field_name] = {
                "original": field_value,
                "translated": translation_result["translated_text"],
                "detected_language": translation_result["detected_source_language"],
            }
            translation_count += 1

    return {
        "translated_document": translated_document,
        "field_results": field_results,
        "target_language": target_language,
        "fields_translated": translation_count,
    }
