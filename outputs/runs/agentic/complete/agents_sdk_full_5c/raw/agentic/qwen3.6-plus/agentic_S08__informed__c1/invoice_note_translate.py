"""
[LATER-STEP] Translate extracted invoice notes or descriptions using DeepL API.

Uses the DeepL translation API to translate invoice notes, line item descriptions,
and vendor memo fields into a target language.
Provider: DeepL - Translation API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

from __future__ import annotations

import os
from typing import List, Optional

import deepl

from document_models import (
    InvoiceExtractionResult,
    NormalizedExpenseRecord,
)


def _get_deepl_client(auth_key: Optional[str] = None) -> deepl.Translator:
    """Create a DeepL translator client using the API key."""
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise EnvironmentError(
            "DeepL API key not found. Set the DEEPL_AUTH_KEY environment variable."
        )
    return deepl.Translator(key)


def translate_text(
    text: str,
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> str:
    """
    Translate a single text string using the DeepL Translation API.

    Args:
        text: The text to translate.
        target_lang: Target language code (e.g., 'EN', 'DE', 'FR', 'ES', 'JA', 'ZH').
        source_lang: Optional source language code. If None, DeepL auto-detects.
        auth_key: Optional DeepL API key override.

    Returns:
        Translated text string.
    """
    translator = _get_deepl_client(auth_key)

    kwargs = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang

    result = translator.translate_text(text, **kwargs)
    return result.text


def translate_invoice_notes(
    invoice: InvoiceExtractionResult,
    target_lang: str = "EN",
    auth_key: Optional[str] = None,
) -> dict:
    """
    Translate all text fields from an extracted invoice using DeepL API.

    Translates:
    - Line item descriptions
    - Vendor notes/memo from raw_fields
    - Any notes attached to the invoice

    Args:
        invoice: InvoiceExtractionResult from Mindee Invoice OCR.
        target_lang: Target language code for translation.
        auth_key: Optional DeepL API key.

    Returns:
        Dictionary with original and translated values for each field.
    """
    translations = {
        "target_language": target_lang,
        "source_language": None,  # auto-detected
        "line_items": [],
        "vendor_notes": None,
        "invoice_notes": None,
    }

    # Translate line item descriptions
    for item in invoice.line_items:
        if item.description and item.description.strip():
            translated_desc = translate_text(item.description, target_lang, auth_key=auth_key)
            translations["line_items"].append({
                "original": item.description,
                "translated": translated_desc,
            })

    # Translate vendor notes from raw_fields
    raw = invoice.raw_fields
    for key in ["notes", "memo", "vendor_notes", "comments", "description"]:
        if key in raw and raw[key] and str(raw[key]).strip():
            translated = translate_text(str(raw[key]), target_lang, auth_key=auth_key)
            translations["vendor_notes"] = {
                "field": key,
                "original": raw[key],
                "translated": translated,
            }
            break

    return translations


def translate_expense_record_notes(
    expense: NormalizedExpenseRecord,
    target_lang: str = "EN",
    auth_key: Optional[str] = None,
) -> NormalizedExpenseRecord:
    """
    Translate notes and line item descriptions in a normalized expense record.

    Args:
        expense: NormalizedExpenseRecord to translate notes for.
        target_lang: Target language code.
        auth_key: Optional DeepL API key.

    Returns:
        Updated NormalizedExpenseRecord with translated notes.
    """
    translated_notes = None
    if expense.notes and expense.notes.strip():
        translated_notes = translate_text(expense.notes, target_lang, auth_key=auth_key)

    translated_items = []
    for item in expense.line_items:
        translated_item = dict(item)
        desc = item.get("description", "")
        if desc and desc.strip():
            translated_item["description"] = translate_text(desc, target_lang, auth_key=auth_key)
            translated_item["original_description"] = desc
        translated_items.append(translated_item)

    # Create updated record
    updated = NormalizedExpenseRecord(**expense.model_dump())
    if translated_notes:
        updated.notes = translated_notes
    updated.line_items = translated_items

    return updated


def batch_translate_texts(
    texts: List[str],
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> List[str]:
    """
    Batch translate multiple texts using DeepL API for efficiency.

    Args:
        texts: List of text strings to translate.
        target_lang: Target language code.
        source_lang: Optional source language code for auto-detect override.
        auth_key: Optional DeepL API key.

    Returns:
        List of translated strings in the same order as input.
    """
    translator = _get_deepl_client(auth_key)

    kwargs = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang

    if not texts:
        return []

    results = translator.translate_text(texts, **kwargs)
    return [r.text for r in results]
