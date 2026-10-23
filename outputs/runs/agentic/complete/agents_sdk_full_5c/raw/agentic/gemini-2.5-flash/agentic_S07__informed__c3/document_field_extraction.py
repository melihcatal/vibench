import os
from google.cloud import documentai_v1beta3 as documentai

def extract_structured_fields(project_id: str, location: str, processor_id: str, file_path: str) -> dict:
    """
    Extracts structured fields from an OCR-normalized document using a specialized Document AI processor
    (e.g., Invoice Parser, Receipt Parser).
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Assuming PDF

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)

    extracted_fields = {}
    for entity in result.document.entities:
        # Entities from specialized processors often have well-defined types and values
        key = entity.type_
        value = result.document.get_text(entity.text_anchor) if entity.text_anchor.text_segments else None
        
        # Normalized values are available for certain field types (e.g., dates, amounts)
        normalized_value = entity.normalized_value.text if entity.normalized_value else None

        # For more complex entities (like line items in invoices), you'd iterate through properties
        # For simplicity, we store basic key-value or normalized value.
        extracted_fields[key] = normalized_value if normalized_value else value

    return extracted_fields

if __name__ == '__main__':
    # Placeholder for direct execution
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"
    # Use a specific processor like 'invoice-parser' or 'receipt-parser'
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID_INVOICE") 

    # Example: fields = extract_structured_fields(project_id, location, processor_id, "path/to/your/invoice.pdf")
    # print("Extracted Fields:", fields)
