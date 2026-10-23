from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
import os

def extract_receipt_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts merchant, tax, total, and items from a receipt using Google Cloud Document AI.
    """

    # Set up client options to specify the region
    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # The full resource name of the processor
    # e.g. projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image_file:
        content = image_file.read()

    raw_document = documentai.RawDocument(content=content, mime_type="application/pdf") # Assuming PDF for receipts, adjust if needed

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    merchant_name = ""
    total_amount = ""
    tax_amount = ""
    line_items = []

    # Iterate over the entities in the document
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
        "merchant_name": merchant_name,
        "total_amount": total_amount,
        "tax_amount": tax_amount,
        "line_items": line_items,
    }

