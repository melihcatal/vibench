import os
from google.cloud import documentai_v1beta3 as documentai
from typing import Dict, Any

def extract_structured_fields_from_invoice(project_id: str, location: str, processor_id: str, file_path: str) -> Dict[str, Any]:
    """
    Extracts structured fields from an invoice document using Google Document AI Invoice Parser.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Assuming PDF for simplicity

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)

    document = result.document
    extracted_fields = {}

    # Iterate through entities to extract structured fields
    for entity in document.entities:
        # Accessing normalized values and confidence for better quality extraction
        field_name = entity.type_
        field_value = entity.normalized_value.text if entity.normalized_value else entity.text_anchor.content if entity.text_anchor else ""
        extracted_fields[field_name] = {
            "value": field_value,
            "confidence": entity.confidence
        }
        # For composite entities like line items, you might need to iterate through properties
        if entity.properties:
            properties = {}
            for prop in entity.properties:
                prop_name = prop.type_
                prop_value = prop.normalized_value.text if prop.normalized_value else prop.text_anchor.content if prop.text_anchor else ""
                properties[prop_name] = {"value": prop_value, "confidence": prop.confidence}
            if field_name not in extracted_fields:
                extracted_fields[field_name] = {}
            extracted_fields[field_name]["properties"] = properties

    return extracted_fields

if __name__ == '__main__':
    # Placeholder for actual usage, demonstrating the provider integration
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us" # e.g., "us"
    processor_id = os.environ.get("DOCUMENTAI_INVOICE_PROCESSOR_ID") # e.g., "invoice-parser"
    file_to_process = "path/to/your/invoice.pdf" # Replace with your invoice document path

    if project_id and processor_id and os.path.exists(file_to_process):
        print(f"Extracting structured fields from {file_to_process} using Google Document AI Invoice Parser...")
        # fields = extract_structured_fields_from_invoice(project_id, location, processor_id, file_to_process)
        # print("Extracted Fields:", json.dumps(fields, indent=2))
    else:
        print("Please set GOOGLE_CLOUD_PROJECT, DOCUMENTAI_INVOICE_PROCESSOR_ID environment variables and ensure the file exists.")
