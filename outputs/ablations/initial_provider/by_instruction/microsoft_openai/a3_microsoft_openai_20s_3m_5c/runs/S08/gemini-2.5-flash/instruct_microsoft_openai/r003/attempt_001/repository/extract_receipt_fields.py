import os
from document_client import get_documentai_client
from document_models import ExtractedReceipt
from typing import Dict, Any, List

def extract_receipt_fields(file_content: bytes, mime_type: str) -> ExtractedReceipt:
    client = get_documentai_client()
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us") # e.g., "us" or "eu"
    processor_id = os.getenv("DOCUMENTAI_RECEIPT_PROCESSOR_ID") # Specific Document AI processor for receipts

    if not project_id or not processor_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT and DOCUMENTAI_RECEIPT_PROCESSOR_ID environment variables must be set.")

    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory.
    document = documentai.RawDocument(
        content=file_content,
        mime_type=mime_type # e.g., "application/pdf", "image/jpeg", "image/png"
    )

    # Configure the process request.
    request = documentai.ProcessRequest(
        name=name,
        raw_document=document,
    )

    result = client.process_document(request=request)
    document_response = result.document

    merchant_name = ""
    total_amount = 0.0
    tax_amount = None
    items: List[Dict[str, Any]] = []

    for entity in document_response.entities:
        if entity.type == "merchant_name":
            merchant_name = entity.mention_text
        elif entity.type == "total_amount":
            try:
                total_amount = float(entity.mention_text)
            except ValueError:
                pass
        elif entity.type == "tax_amount":
            try:
                tax_amount = float(entity.mention_text)
            except ValueError:
                pass
        elif entity.type == "line_item":
            item_data = {}
            for prop in entity.properties:
                if prop.type == "description":
                    item_data["description"] = prop.mention_text
                elif prop.type == "price":
                    try:
                        item_data["price"] = float(prop.mention_text)
                    except ValueError:
                        pass
            if item_data: # Only add if some data was extracted for the item
                items.append(item_data)

    return ExtractedReceipt(
        merchant=merchant_name,
        total=total_amount,
        tax=tax_amount,
        items=items
    )
