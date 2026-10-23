from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
import os

def extract_receipt_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts merchant, tax, total, and items from a receipt using Google Cloud Document AI.
    """
    
    # You can set the endpoint for regionalization, e.g., "eu-documentai.googleapis.com"
    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)
    
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    document = documentai.RawDocument(
        content=image_content, 
        mime_type="application/pdf" # Assuming receipts can be PDFs, adjust if needed
    )

    request = documentai.ProcessRequest(name=name, raw_document=document)

    result = client.process_document(request=request)
    
    document = result.document
    
    # Initialize fields
    merchant_name = None
    total_amount = None
    tax_amount = None
    line_items = []

    # Extract fields from entities
    for entity in document.entities:
        if entity.type_ == "merchant_name":
            merchant_name = entity.mention_text
        elif entity.type_ == "total_amount":
            total_amount = entity.mention_text
        elif entity.type_ == "tax_amount":
            tax_amount = entity.mention_text
        elif entity.type_ == "line_item":
            item = {}
            for prop in entity.properties:
                if prop.type_ == "description":
                    item["description"] = prop.mention_text
                elif prop.type_ == "amount":
                    item["amount"] = prop.mention_text
            if item:
                line_items.append(item)

    return {
        "merchant_name": merchant_name,
        "total_amount": total_amount,
        "tax_amount": tax_amount,
        "line_items": line_items,
    }

