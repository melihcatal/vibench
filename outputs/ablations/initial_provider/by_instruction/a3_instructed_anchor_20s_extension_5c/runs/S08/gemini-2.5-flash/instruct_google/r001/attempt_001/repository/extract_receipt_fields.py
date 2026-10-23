import os
from document_client import get_documentai_receipt_client
from document_models import Receipt, LineItem
from google.cloud import documentai_v1 as documentai

def extract_receipt_fields(file_path: str) -> Receipt:
    client, processor_name = get_documentai_receipt_client()

    with open(file_path, "rb") as image_file:
        image_content = image_file.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Assuming PDF, adjust if other types are expected

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    result = client.process_document(request=request)

    document = result.document
    receipt = Receipt()

    # Extracting document-level fields
    for entity in document.entities:
        if entity.type == "merchant_name":
            receipt.merchant_name = entity.mention_text
        elif entity.type == "transaction_date":
            receipt.transaction_date = entity.mention_text
        elif entity.type == "total_amount":
            try:
                receipt.total_amount = float(entity.mention_text)
            except (ValueError, TypeError):
                pass
        elif entity.type == "tax_amount":
            try:
                receipt.tax_amount = float(entity.mention_text)
            except (ValueError, TypeError):
                pass
        elif entity.type == "line_item":
            line_item = LineItem(description=entity.mention_text)
            for prop in entity.properties:
                if prop.type == "description":
                    line_item.description = prop.mention_text
                elif prop.type == "quantity":
                    try:
                        line_item.quantity = float(prop.mention_text)
                    except (ValueError, TypeError):
                        pass
                elif prop.type == "unit_price":
                    try:
                        line_item.unit_price = float(prop.mention_text)
                    except (ValueError, TypeError):
                        pass
                elif prop.type == "total_price":
                    try:
                        line_item.total_price = float(prop.mention_text)
                    except (ValueError, TypeError):
                        pass
            receipt.items.append(line_item)

    return receipt
