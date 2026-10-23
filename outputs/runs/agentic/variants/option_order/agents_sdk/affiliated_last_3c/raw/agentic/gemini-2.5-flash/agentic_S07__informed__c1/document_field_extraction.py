import os
from google.cloud import documentai_v1 as documentai

def extract_structured_fields_from_invoice(project_id: str, location: str, file_path: str):
    """
    Extracts structured fields from an invoice document using Google Document AI Invoice Parser.
    """
    # The invoice processor ID is a special one provided by Document AI for pre-built models.
    # For Invoice Parser, the processor ID is typically constant or you create one in the console.
    # Using a common pre-trained processor, you might just need the processor type name.
    # For programmatic access to specific pre-built processors, you often use the processor type.
    # We'll assume a specific processor_id is configured, which maps to the Invoice Parser.
    # In practice, you might create an Invoice Parser in the console and use its ID.
    invoice_processor_id = os.environ.get("DOCUMENT_AI_INVOICE_PROCESSOR_ID", "YOUR_INVOICE_PROCESSOR_ID")
    
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, invoice_processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf", # Invoices are often PDFs
        ),
    )

    result = client.process_document(request=request)
    document = result.document

    extracted_fields = {}

    for entity in document.entities:
        # Accessing entities for structured data extraction
        # The specific fields depend on the processor (e.g., Invoice Parser)
        # Common fields for invoices include vendor_name, total_amount, invoice_id, etc.
        if entity.type_ != "": # Only process entities with a defined type
            # The `mention_text` or `normalized_value` provide the extracted data
            value = entity.mention_text if entity.mention_text else entity.normalized_value.text if entity.normalized_value else ""
            extracted_fields[entity.type_] = value

            # You can also access confidence scores, page references, etc.
            # print(f"  Type: {entity.type_}, Value: {value}, Confidence: {entity.confidence}")

    return extracted_fields

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"
    file_to_process = "path/to/your/invoice.pdf"

    if project_id and os.path.exists(file_to_process):
        # Ensure DOCUMENT_AI_INVOICE_PROCESSOR_ID is set in environment or replace placeholder
        # This should be the ID of an 'Invoice Parser' processor created in Document AI console.
        invoice_processor_id = os.environ.get("DOCUMENT_AI_INVOICE_PROCESSOR_ID")
        if not invoice_processor_id or invoice_processor_id == "YOUR_INVOICE_PROCESSOR_ID":
            print("Please set DOCUMENT_AI_INVOICE_PROCESSOR_ID environment variable with your Invoice Parser ID.")
        else:
            structured_data = extract_structured_fields_from_invoice(project_id, location, file_to_process)
            print("Extracted Structured Fields from Invoice:")
            import json
            print(json.dumps(structured_data, indent=2))
    else:
        print("Please set GOOGLE_CLOUD_PROJECT environment variable and ensure invoice file exists.")
