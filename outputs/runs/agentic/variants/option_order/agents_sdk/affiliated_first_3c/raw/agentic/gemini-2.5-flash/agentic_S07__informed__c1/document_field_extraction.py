import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_processor_path

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str) -> dict:
    """Extracts structured fields from an invoice document using Google Document AI's Invoice Parser."""
    client = get_documentai_client()
    # The processor_id here should correspond to a 'Invoice Parser' processor (e.g., invoice-parser-v1.0).
    processor_path = get_processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    document = documentai.RawDocument(content=image_content, mime_type="application/pdf")
    request = documentai.ProcessRequest(name=processor_path, raw_document=document)

    response = client.process_document(request=request)
    doc = response.document

    extracted_fields = {}

    # Iterate through entities to find specific invoice fields
    for entity in doc.entities:
        # Entities have different types for invoices, like 'supplier_name', 'total_amount', etc.
        # The `text_anchor` points to the original text in the document.
        if entity.type_ in ["total_amount", "invoice_id", "supplier_name", "invoice_date"]:
            value = ""
            if entity.mention_text_anchor.text_segments:
                value = doc.text[entity.mention_text_anchor.text_segments[0].start_index:entity.mention_text_anchor.text_segments[0].end_index]
            extracted_fields[entity.type_] = value
        # For line items, it's more complex and requires iterating through properties.
        # This example focuses on top-level fields.

    return extracted_fields

if __name__ == '__main__':
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    LOCATION = "us"
    # Use an Invoice Parser Processor ID (e.g., 'invoice-parser-v1.0')
    PROCESSOR_ID = os.getenv("DOCUMENTAI_INVOICE_PROCESSOR_ID", "your-invoice-processor-id") # e.g., "invoice-parser-v1.0"
    SAMPLE_FILE = "path/to/your/invoice.pdf"

    # invoice_data = extract_invoice_fields(PROJECT_ID, LOCATION, PROCESSOR_ID, SAMPLE_FILE)
    # for field, value in invoice_data.items():
    #     print(f"{field}: {value}")
