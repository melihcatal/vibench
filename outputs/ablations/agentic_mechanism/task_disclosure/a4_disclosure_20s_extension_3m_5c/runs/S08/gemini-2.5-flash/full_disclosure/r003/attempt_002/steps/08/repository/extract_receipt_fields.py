from google.cloud import documentai_v1 as documentai
import os

def extract_receipt_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts merchant, tax, total, and items from a receipt using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The location of the processor (e.g., "us").
        processor_id: The ID of the Document AI processor configured for receipts.
        file_path: The path to the receipt file.

    Returns:
        A dictionary containing the extracted merchant, tax, total, and items.
    """
    
    # Create a client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g., projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Adjust mime_type if needed

    # Use the process_document method
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)
    result = client.process_document(request=request)

    document = result.document

    merchant_name = ""
    tax_amount = 0.0
    total_amount = 0.0
    items = []

    # Extract fields based on Document AI's schema for receipts
    for entity in document.entities:
        if entity.type == "merchant_name":
            merchant_name = entity.mention_text
        elif entity.type == "total_amount":
            total_amount = float(entity.mention_text)
        elif entity.type == "tax_amount":
            tax_amount = float(entity.mention_text)
        elif entity.type == "line_item":
            item = {}
            for prop in entity.properties:
                if prop.type == "item_description":
                    item["description"] = prop.mention_text
                elif prop.type == "item_amount":
                    item["amount"] = float(prop.mention_text)
            if item:
                items.append(item)

    return {
        "merchant_name": merchant_name,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
        "items": items,
    }

