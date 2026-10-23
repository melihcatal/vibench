from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
import os

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str) -> dict:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.
    """
    # You can set the endpoint to a specific region, e.g., "us-documentai.googleapis.com"
    # For more options, see: https://cloud.google.com/document-ai/docs/regions
    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # The full resource name of the processor
    # e.g., projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=resource_name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf"  # Or "image/jpeg", "image/png", etc.
        ),
    )

    result = client.process_document(request=request)
    document = result.document

    # Initialize extracted fields
    extracted_data = {
        "vendor": None,
        "date": None,
        "total": None,
        "line_items": []
    }

    # Extract fields
    for entity in document.entities:
        if entity.type == "supplier_name" and entity.mention_text:
            extracted_data["vendor"] = entity.mention_text
        elif entity.type == "invoice_date" and entity.mention_text:
            extracted_data["date"] = entity.mention_text
        elif entity.type == "total_amount" and entity.mention_text:
            extracted_data["total"] = entity.mention_text
        elif entity.type == "line_item":
            line_item = {}
            for sub_entity in entity.properties:
                if sub_entity.type == "description" and sub_entity.mention_text:
                    line_item["description"] = sub_entity.mention_text
                elif sub_entity.type == "quantity" and sub_entity.mention_text:
                    line_item["quantity"] = sub_entity.mention_text
                elif sub_entity.type == "unit_price" and sub_entity.mention_text:
                    line_item["unit_price"] = sub_entity.mention_text
                elif sub_entity.type == "amount" and sub_entity.mention_text:
                    line_item["amount"] = sub_entity.mention_text
            if line_item:
                extracted_data["line_items"].append(line_item)

    return extracted_data
