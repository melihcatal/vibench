# [SAME-SCENARIO] extract_receipt_fields.py

# Uses Google Document AI Receipt Parser (prebuilt)
# SDK: google-cloud-documentai

import os
from google.cloud import documentai

assert "GOOGLE_APPLICATION_CREDENTIALS" in os.environ, (
    "Set GOOGLE_APPLICATION_CREDENTIALS"
)


def extract_receipt_fields(file_path: str):
    """Extract merchant, tax, total, and items from a receipt using Google Document AI.

    Returns dict with keys: merchant, tax_amount, total_amount, items (list).
    """
    client = documentai.DocumentProcessorServiceClient()
    processor_id = (
        "projects/your-project/locations/us-central1/processors/your_receipt_processor"
    )
    with open(file_path, "rb") as receipt:
        raw_doc = documentai.Document.from_bytes(receipt.read())
    response = client.process_document(name=processor_id, raw_document=raw_doc)
    doc = response.document
    # Simple field extraction (replace with actual locations)
    merchant = doc.pages[0].blocks[0].text  # placeholder
    tax_amount = doc.pages[0].blocks[1].text  # placeholder
    total_amount = doc.pages[0].blocks[2].text  # placeholder
    items = []
    for item in doc.pages[0].tables[0].body_rows:
        items.append(
            {
                "description": item.cells[0].text,
                "quantity": item.cells[1].text,
                "price": item.cells[2].text,
            }
        )
    return {
        "merchant": merchant,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
        "items": items,
    }
