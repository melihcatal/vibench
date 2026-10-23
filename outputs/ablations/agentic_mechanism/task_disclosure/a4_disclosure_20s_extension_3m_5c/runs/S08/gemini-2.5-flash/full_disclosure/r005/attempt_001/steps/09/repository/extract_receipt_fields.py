from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
import os

def extract_receipt_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts merchant, tax, total, and items from a receipt using Google Cloud Document AI.
    """
    
    # You can set this env variable to use a different endpoint if needed.
    # For example: documentai_client_options = ClientOptions(api_endpoint="eu-documentai.googleapis.com")
    documentai_client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=documentai_client_options)

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    processor_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf",  # Adjust mime_type as per your document type
        ),
    )

    result = client.process_document(request=request)
    document = result.document

    merchant_name = ""
    total_amount = ""
    tax_amount = ""
    line_items = []

    for entity in document.entities:
        if entity.type == "merchant_name":
            merchant_name = entity.mention_text
        elif entity.type == "total_amount":
            total_amount = entity.mention_text
        elif entity.type == "tax_amount":
            tax_amount = entity.mention_text
        elif entity.type == "line_item":
            item = {}
            for prop in entity.properties:
                if prop.type == "description":
                    item["description"] = prop.mention_text
                elif prop.type == "amount":
                    item["amount"] = prop.mention_text
            if item:
                line_items.append(item)

    return {
        "merchant": merchant_name,
        "tax": tax_amount,
        "total": total_amount,
        "items": line_items,
    }

