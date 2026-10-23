# [SAME-SCENARIO] extract_invoice_fields.py
"""
Extract vendor, date, total, and line-item fields from an invoice using Google Vision Document AI.
"""
import json
from google.cloud import documentai
from document_models import InvoiceExtractionRequest, InvoiceExtractionResponse

def extract_invoice_fields(invoice_path: str) -> InvoiceExtractionResponse:
    """Extract structured fields from a PDF invoice.

    Args:
        invoice_path: Path to the invoice PDF file.

    Returns:
        InvoiceExtractionResponse containing vendor, date, total, and line items.
    """
    # Initialize Document AI client with service account credentials
    client = documentai.DocumentProcessorServiceClient()
    # Example of using an environment variable for the processor ID (provider-specific)
    processor_id = "projects/PROJECT/locations/us/processors/INVOICE_PROCESSOR"
    with open(invoice_path, "rb") as image:
        image_content = image.read()
    # Prepare the request
    name = f"{processor_id}:process"
    request = documentai.types.ProcessDocumentRequest(
        name=name,
        document={'content': image_content, 'mime_type': "application/pdf"},
    )
    # Send request and get response
    response = client.process_document(request=request)
    # Parse vendor, date, total, and line items from the response (placeholder logic)
    vendor = "Acme Corp"  # placeholder
    date = "2024-07-01"   # placeholder
    total = 123.45         # placeholder
    line_items = [{"description": "Item A", "quantity": 2, "unit_price": 10.0}]  # placeholder
    return InvoiceExtractionResponse(
        vendor=vendor,
        date=date,
        total=total,
        line_items=line_items,
    )
