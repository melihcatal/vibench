from google.cloud import documentai_v1beta3 as documentai
import os

def extract_fields_from_receipt(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts merchant, tax, total, and items from a receipt using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The location of the processor (e.g., "us").
        processor_id: The ID of the specialized receipt processor.
        file_path: The path to the receipt image file.

    Returns:
        A dictionary containing the extracted merchant, tax, total, and items,
        or None if extraction fails.
    """
    client = documentai.DocumentProcessorServiceClient()

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image_file:
        image_content = image_file.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Assuming PDF, adjust if different image type

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    merchant_name = None
    total_amount = None
    tax_amount = None
    line_items = []

    # Extract entities
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
                elif prop.type == "price":
                    item["price"] = prop.mention_text
                elif prop.type == "quantity":
                    item["quantity"] = prop.mention_text
            if item:
                line_items.append(item)

    return {
        "merchant": merchant_name,
        "tax": tax_amount,
        "total": total_amount,
        "items": line_items,
    }

