# [SAME-SCENARIO] extract_receipt_fields.py
# Extracts merchant, tax, total, and items from a receipt using Mindee Invoice OCR

import mindee
from document_client import MindeeClient
from document_models import ReceiptExtractionResult


def extract_receipt_fields(receipt_bytes):
    """Extract structured fields from a receipt image using Mindee Invoice OCR.

    Args:
        receipt_bytes (bytes): Raw bytes of the receipt image.

    Returns:
        ReceiptExtractionResult: Normalized extraction result.
    """
    client = MindeeClient()
    doc = client.process(receipt_bytes)
    # Transform Mindee response into normalized result
    return ReceiptExtractionResult.from_mindee(doc)
