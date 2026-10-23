from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
import os

def extract_receipt_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts merchant, tax, total, and items from a receipt using Google Cloud Document AI.
    """

    # Set up client options
    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # The full resource name of the processor
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image_file:
        content = image_file.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=resource_name,
        raw_document=documentai.RawDocument(
            content=content,
            mime_type="application/pdf" # or "image/jpeg", "image/png" etc.
        )
    )

    result = client.process_document(request=request)
    document = result.document

    merchant_name = ""
    total_amount = ""
    tax_amount = ""
    items = []

    # Extract fields from entities
    for entity in document.entities:
        if entity.type_ == "merchant_name":
            merchant_name = entity.mention_text
        elif entity.type_ == "total_amount":
            total_amount = entity.mention_text
        elif entity.type_ == "tax_amount":
            tax_amount = entity.mention_text
        elif entity.type_ == "line_item":
            item_description = ""
            item_price = ""
            for prop in entity.properties:
                if prop.type_ == "line_item_description":
                    item_description = prop.mention_text
                elif prop.type_ == "line_item_amount":
                    item_price = prop.mention_text
            items.append({"description": item_description, "price": item_price})

    return {
        "merchant": merchant_name,
        "tax": tax_amount,
        "total": total_amount,
        "items": items,
    }

