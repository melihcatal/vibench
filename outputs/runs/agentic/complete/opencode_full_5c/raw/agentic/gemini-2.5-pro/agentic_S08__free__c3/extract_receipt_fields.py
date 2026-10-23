from typing import Optional
import os
from document_client import get_documentai_client
from document_models import Receipt, ReceiptItem


def extract_receipt_fields(file_path: str) -> Optional[Receipt]:
    """
    Extracts fields from a receipt document using Google Document AI.
    """
    client = get_documentai_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.environ.get("DOCAI_RECEIPT_PROCESSOR_ID")

    if not all([project_id, location, processor_id]):
        raise ValueError("Missing Google Cloud or Document AI configuration.")

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = {"content": image_content, "mime_type": "image/jpeg"}

    request = {"name": name, "raw_document": raw_document}
    result = client.process_document(request=request)
    document = result.document

    receipt = Receipt()

    for entity in document.entities:
        if entity.type_ == "receipt_date":
            # Not in our model, but shows parsing
            pass
        elif entity.type_ == "supplier_name":
            receipt.merchant_name = entity.mention_text
        elif entity.type_ == "total_amount":
            receipt.total = float(entity.mention_text)
        elif entity.type_ == "total_tax_amount":
            receipt.tax = float(entity.mention_text)
        elif entity.type_ == "line_item":
            item = ReceiptItem(description="", total=0.0)
            for prop in entity.properties:
                if prop.type_ == "line_item/description":
                    item.description = prop.mention_text
                elif prop.type_ == "line_item/amount":
                    item.total = float(prop.mention_text)
            if item.description:
                receipt.items.append(item)
    return receipt
