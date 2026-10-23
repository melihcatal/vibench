# [SAME-SCENARIO] extract_invoice_fields.py
# Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI
import os
from google.cloud import documentai_v1 as documentai

# Set up client (uses environment variable GOOGLE_APPLICATION_CREDENTIALS)
client = documentai.DocumentAnalyzerClient()


def extract_invoice_fields(pdf_bytes: bytes) -> dict:
    """Extract structured fields from a PDF invoice.

    Returns a dict with keys: vendor, date, total, line_items.
    """
    # Construct the document
    document = {"content": pdf_bytes, "mime_type": "application/pdf"}
    # Define processor (example: `invoice-parser` - replace with your actual processor ID)
    processor_name = (
        "projects/PROJECT_ID/locations/us-central1/processors/INVOICE_PARSER"
    )
    # Send request
    response = client.process_document(
        request={"name": processor_name, "document": document}
    )
    document = response.document

    # Simple extraction logic (adjust based on your schema)
    vendor = None
    date = None
    total = None
    line_items = []
    for entity in document.entities:
        # Example heuristic – replace with actual field mapping
        if entity.type_ == "VENDOR":
            vendor = entity.confidence
        elif entity.type_ == "DATE":
            date = entity.confidence
        elif entity.type_ == "TOTAL":
            total = entity.confidence
        elif entity.type_ == "LINE_ITEM":
            line_items.append(entity.confidence)

    return {
        "vendor": vendor,
        "date": date,
        "total": total,
        "line_items": line_items,
    }
