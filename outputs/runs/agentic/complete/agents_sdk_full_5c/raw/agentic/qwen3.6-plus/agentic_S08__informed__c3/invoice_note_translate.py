"""Translate extracted invoice notes or descriptions using DeepL API.

Uses the DeepL translation service (deepl SDK) to translate invoice notes,
vendor memos, or line item descriptions between supported languages.
Auth env var: DEEPL_AUTH_KEY
"""

import os
import json
from typing import Optional, List
import deepl
from document_models import InvoiceExtractionResult


def translate_invoice_notes(
    extraction: InvoiceExtractionResult,
    target_lang: str = "EN-US",
    source_lang: Optional[str] = None,
) -> dict:
    """Translate invoice notes and descriptions using DeepL API.

    Translates vendor name, notes, memo, and line item descriptions from
    the source language to the target language.

    Args:
        extraction: InvoiceExtractionResult containing extracted fields.
        target_lang: Target language code (e.g., 'EN-US', 'DE', 'FR', 'JA').
        source_lang: Source language code (auto-detected if None).

    Returns:
        Dictionary with translated fields.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY environment variable is not set")

    translator = deepl.Translator(auth_key)

    texts_to_translate = {}

    vendor_name = extraction.vendor_name or extraction.raw_fields.get("VendorName", "")
    if vendor_name:
        texts_to_translate["vendor_name"] = vendor_name

    notes = extraction.raw_fields.get("Notes", "")
    if notes:
        texts_to_translate["notes"] = notes

    memo = extraction.raw_fields.get("Memo", "")
    if memo:
        texts_to_translate["memo"] = memo

    for i, item in enumerate(extraction.line_items):
        if item.description:
            texts_to_translate[f"item_{i}_description"] = item.description

    if not texts_to_translate:
        return {
            "target_lang": target_lang,
            "source_lang": source_lang or "auto",
            "translations": {},
            "note": "No text content to translate",
        }

    translations = {}

    translate_options = {}
    if source_lang:
        translate_options["source_lang"] = source_lang
    translate_options["target_lang"] = target_lang

    for key, text in texts_to_translate.items():
        result = translator.translate_text(text, **translate_options)
        translations[key] = result.text

    detected_source = translations.get("_detected_source", source_lang or "auto")
    if source_lang is None:
        first_result = translator.translate_text(
            texts_to_translate.get("vendor_name", texts_to_translate.get("notes", "")),
            target_lang=target_lang,
            split_sentences="nonewlines",
        )
        if hasattr(first_result, "detected_source_lang"):
            detected_source = first_result.detected_source_lang

    return {
        "target_lang": target_lang,
        "source_lang": detected_source or "auto",
        "translations": translations,
        "translated_vendor_name": translations.get("vendor_name", ""),
        "translated_notes": translations.get("notes", ""),
        "translated_memo": translations.get("memo", ""),
        "translated_line_items": [
            {
                "description": translations.get(f"item_{i}_description", item.description),
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "amount": item.amount,
            }
            for i, item in enumerate(extraction.line_items)
        ],
    }


def translate_text_only(
    text: str,
    target_lang: str = "EN-US",
    source_lang: Optional[str] = None,
) -> str:
    """Translate a single text string using DeepL API.

    Args:
        text: Text to translate.
        target_lang: Target language code.
        source_lang: Source language code (auto-detected if None).

    Returns:
        Translated text string.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY environment variable is not set")

    translator = deepl.Translator(auth_key)

    translate_kwargs = {"target_lang": target_lang}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang

    result = translator.translate_text(text, **translate_kwargs)
    return result.text


if __name__ == "__main__":
    import sys
    sample = sys.argv[1] if len(sys.argv) > 1 else "Bitte bezahlen Sie diese Rechnung innerhalb von 30 Tagen."
    result = translate_text_only(sample, target_lang="EN-US")
    print(result)
