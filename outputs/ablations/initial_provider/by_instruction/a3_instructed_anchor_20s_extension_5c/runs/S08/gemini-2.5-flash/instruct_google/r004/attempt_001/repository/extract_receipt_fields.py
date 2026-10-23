import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import Receipt, LineItem

def extract_receipt_fields(document_content: bytes, mime_type: str) -> Receipt:
    client = get_documentai_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    processor_id = os.getenv("GOOGLE_CLOUD_RECEIPT_PROCESSOR_ID") # Specific processor for receipts

    if not processor_id:
        raise ValueError("GOOGLE_CLOUD_RECEIPT_PROCESSOR_ID environment variable must be set.")

    resource_name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=document_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    receipt = Receipt()

    for entity in document.entities:
        if entity.type == "merchant_name":
            receipt.merchant_name = entity.mention_text
        elif entity.type == "transaction_date":
            receipt.transaction_date = entity.mention_text
        elif entity.type == "total_amount":
            receipt.total_amount = float(entity.mention_text) if entity.mention_text else None
            if entity.normalized_value and entity.normalized_value.currency_symbol:
                receipt.currency = entity.normalized_value.currency_symbol
        elif entity.type == "total_tax": # Document AI often returns total_tax for receipts
            receipt.tax_amount = float(entity.mention_text) if entity.mention_text else None
        elif entity.type == "line_item":
            line_item = LineItem()
            for prop in entity.properties:
                if prop.type == "description":
                    line_item.description = prop.mention_text
                elif prop.type == "quantity":
                    line_item.quantity = float(prop.mention_text) if prop.mention_text else None
                elif prop.type == "unit_price":
                    line_item.unit_price = float(prop.mention_text) if prop.mention_text else None
                elif prop.type == "line_item_amount":
                    line_item.total_price = float(prop.mention_text) if prop.mention_text else None
            receipt.items.append(line_item)
            
    return receipt
