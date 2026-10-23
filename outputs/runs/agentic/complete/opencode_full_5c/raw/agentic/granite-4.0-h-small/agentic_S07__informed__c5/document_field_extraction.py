# [LATER-STEP] document_field_extraction.py

import os
from document_client import DocumentClient
from document_models import OcrResult, normalize_ocr_response

# --------------------------------------------------------------------------
# This module demonstrates extracting structured fields from a generic OCR result.
# --------------------------------------------------------------------------


def extract_fields_from_ocr(ocr_result: OcrResult) -> dict:
    """Convert generic OCR dict to a flat dictionary of field names/values.

    Args:
        ocr_result: Normalized OCR output (text, fields, tables, raw).

    Returns:
        Dictionary mapping extracted field names to their values.
    """
    # If the provider already supplied 'fields', just return them.
    if ocr_result.fields:
        return ocr_result.fields
    # Fallback: simple heuristic for Mindee (key/value items)
    raw = ocr_result.raw
    kv = {}
    # Example heuristic for Mindee key/value extraction
    if raw.get("fields"):
        for key_entry in raw["fields"].get("key", []):
            key = key_entry.get("text", "")
            # Find matching value entry by proximity (simplified)
            for value_entry in raw.get("fields", {}).get("value", []):
                if value_entry.get("page_index") == key_entry.get("page_index"):
                    kv[key] = value_entry.get("text", "")
    return kv


def main():
    # Example: use Google Document AI form parsing as source (returns dict)
    client = DocumentClient(service="google_document_ai")
    raw = client.ocr("sample_form.jpg")
    # Normalize to our generic envelope
    norm = normalize_ocr_response(provider="google_document_ai", raw_response=raw)
    fields = extract_fields_from_ocr(norm)
    print("Extracted Fields:")
    print(fields)


if __name__ == "__main__":
    main()
