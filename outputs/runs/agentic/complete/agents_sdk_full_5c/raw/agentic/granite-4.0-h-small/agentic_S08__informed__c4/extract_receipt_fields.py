# [SAME-SCENARIO] extract_receipt_fields.py
import os
from mindee import MindeeClient
from document_models import ReceiptExtractionResponse

def extract_receipt_fields(image_bytes: bytes) -> ReceiptExtractionResponse:
    """Extract merchant, tax, total, and items from a receipt image using Mindee Invoice OCR.

    Returns a structured response matching the ReceiptExtractionResponse schema.
    """
    client = MindeeClient(api_key=os.getenv('MINDEE_API_KEY'))
    raw_resp = client.invoice_ocr(image_bytes)
    # Map raw Mindee response to our schema
    return map_to_receipt_response(raw_resp)

def map_to_receipt_response(raw: dict) -> ReceiptExtractionResponse:
    # Adjust field names to match Mindee output structure
    return ReceiptExtractionResponse(
        merchant=raw.get('merchant', ''),
        tax=raw.get('tax', ''),
        total=raw.get('total', ''),
        items=raw.get('items', [])
    )