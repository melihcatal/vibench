import os
from typing import List
from google.cloud import documentai

from document_client import get_google_document_ai_client
from document_models import ExtractedInvoice, InvoiceLineItem


def extract_invoice_from_file(
    file_path: str,
    gcp_project_id: str,
    gcp_location: str,
    gcp_processor_id: str,
    mime_type: str = "application/pdf",
) -> ExtractedInvoice:
    """
    Extracts structured data from an invoice PDF using Google Document AI.
    """
    client = get_google_document_ai_client(gcp_project_id, gcp_location)

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processors/processor-id
    # You must create new processors in the Cloud Console.
    name = client.processor_path(gcp_project_id, gcp_location, gcp_processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    # Read the file into memory
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    # Parse the results
    raw_fields = {
        entity.type_: entity.mention_text for entity in document.entities
    }
    
    line_items = []
    # This is a simplified example; real line item parsing is more complex
    if 'line_item' in raw_fields:
        # A real implementation would parse the nested structure of line items
        pass

    invoice = ExtractedInvoice(
        vendor_name=raw_fields.get("vendor_name"),
        invoice_id=raw_fields.get("invoice_id"),
        invoice_date=raw_fields.get("invoice_date"),
        due_date=raw_fields.get("due_date"),
        total_amount=float(raw_fields.get("total_amount", 0)),
        tax_amount=float(raw_fields.get("tax_amount", 0)),
        line_items=line_items,
        raw_fields=raw_fields,
    )
    return invoice

# Example usage would require a file and GCP credentials.
# The model is identified by the `gcp_processor_id`, which could be a specialized
# one like 'pretrained-invoice-v1.3-2022-07-15' or a custom trained one.
