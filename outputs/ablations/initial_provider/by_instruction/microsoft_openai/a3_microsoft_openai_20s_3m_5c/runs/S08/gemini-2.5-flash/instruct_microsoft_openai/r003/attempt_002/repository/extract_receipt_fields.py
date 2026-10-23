import os
from document_client import get_documentai_client
from document_models import ExtractedReceiptFields, LineItem
from google.cloud import documentai_v1 as documentai

def extract_receipt_fields(project_id: str, location: str, processor_id: str, file_content: bytes) -> ExtractedReceiptFields:
    client = get_documentai_client()
    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=file_content,
        mime_type="application/pdf" # Assuming PDF, could be image as well
    )
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request)
    document = result.document

    merchant_name = None
    tax_amount = None
    total_amount = None
    items = []

    for entity in document.entities:
        if entity.type == "merchant_name":
            merchant_name = entity.mention_text
        elif entity.type == "total_amount":
            try:
                total_amount = float(entity.mention_text)
            except (ValueError, TypeError):
                pass
        elif entity.type == "tax_amount":
            try:
                tax_amount = float(entity.mention_text)
            except (ValueError, TypeError):
                pass
        elif entity.type == "line_item":
            item_description = None
            item_total_price = None
            for prop in entity.properties:
                if prop.type == "description":
                    item_description = prop.mention_text
                elif prop.type == "amount": # Assuming 'amount' for line item total
                    try:
                        item_total_price = float(prop.mention_text)
                    except (ValueError, TypeError):
                        pass
            if item_description or item_total_price:
                items.append(LineItem(description=item_description if item_description else "N/A", total_price=item_total_price))
    
    return ExtractedReceiptFields(
        merchant_name=merchant_name,
        tax_amount=tax_amount,
        total_amount=total_amount,
        items=items
    )
