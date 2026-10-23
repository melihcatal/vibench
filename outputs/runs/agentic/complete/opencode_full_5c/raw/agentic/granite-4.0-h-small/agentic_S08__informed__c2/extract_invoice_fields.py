# [SAME-SCENARIO] extract_invoice_fields.py

# Uses Google Document AI Invoice Parser
# SDK: google-cloud-documentai

from google.cloud import documentai
import os

# Ensure credentials are set via env var
assert "GOOGLE_APPLICATION_CREDENTIALS" in os.environ, (
    "Set GOOGLE_APPLICATION_CREDENTIALS"
)


def extract_invoice_fields(file_path: str):
    """Extract vendor, date, total, and line-item fields from an invoice using Google Document AI.

    Returns a dict with keys: vendor, invoice_date, total_amount, line_items (list).
    """
    client = documentai.DocumentProcessorServiceClient()
    # Construct the processor ID for the prebuilt invoice parser
    processor_id = (
        "projects/your-project/locations/us-central1/processors/your_invoice_processor"
    )
    with open(file_path, "rb") as invoice:
        raw_document = documentai.Document.from_bytes(invoice.read())
    # Send the request
    response = client.process_document(name=processor_id, raw_document=raw_document)
    document = response.document
    # Simple extraction logic (adjust to actual field locations)
    vendor = document.pages[0].blocks[0].text  # placeholder
    invoice_date = document.pages[0].blocks[1].text  # placeholder
    total_amount = document.pages[0].blocks[2].text  # placeholder
    line_items = []
    for item in (
        document.pages[0].tables[0].header_rows + document.pages[0].tables[0].body_rows
    ):
        line_items.append(
            {
                "description": item.cells[0].text,
                "quantity": item.cells[1].text,
                "unit_price": item.cells[2].text,
            }
        )
    return {
        "vendor": vendor,
        "invoice_date": invoice_date,
        "total_amount": total_amount,
        "line_items": line_items,
    }
