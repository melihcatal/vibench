import os
from google.cloud import documentai

# Provider: Google Document AI Invoice Parser


def extract_invoice_fields(pdf_bytes):
    # Initialize Document AI client using env var GOOGLE_APPLICATION_CREDENTIALS
    client = documentai.DocumentProcessorServiceClient()
    # Construct the resource name of the processor.
    processor_id = os.getenv("DOCUMENT_AI_PROCESSOR_ID")
    name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/{os.getenv('GOOGLE_CLOUD_REGION')}/processors/{processor_id}"
    # Prepare the document payload
    document = documentai.Document(content=pdf_bytes, mime_type="application/pdf")
    # Send request to processor
    response = client.process_document(name=name, document=document)
    # Parse invoice fields (simplified example)
    invoice = {}
    for entity in response.document.entities:
        if entity.type_ == "VENDOR":
            invoice["vendor"] = entity.normalized_value
        elif entity.type_ == "DATE":
            invoice["date"] = entity.normalized_value
        elif entity.type_ == "TOTAL":
            invoice["total"] = entity.normalized_value
        elif entity.type_ == "LINE_ITEM_DESCRIPTION":
            # Collect line items
            invoice.setdefault("line_items", []).append(
                {
                    "description": entity.text,
                    "quantity": None,
                    "unit_price": None,
                    "total": None,
                }
            )
    return invoice
