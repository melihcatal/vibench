import os
from typing import Optional, List
from document_client import DocumentClient
from document_models import DocumentPayload, ExtractedReceipt, LineItem
from google.cloud import documentai_v1 as documentai

def extract_receipt_fields(payload: DocumentPayload, config: Optional[dict] = None) -> dict:
    config = config or {}
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
    receipt_processor_id = os.environ.get("GOOGLE_CLOUD_RECEIPT_PROCESSOR_ID")

    if not project_id or not receipt_processor_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_RECEIPT_PROCESSOR_ID must be set in environment variables.")

    doc_client = DocumentClient(project_id, location)
    document = doc_client.process_document(
        receipt_processor_id, payload.document_bytes, payload.mime_type
    )

    merchant_name = None
    total_amount = None
    tax_amount = None
    currency = None
    items: List[LineItem] = []

    if document.entities:
        for entity in document.entities:
            if entity.type == "merchant_name":
                merchant_name = entity.mention_text
            elif entity.type == "total_amount":
                total_amount = float(entity.mention_text) if entity.mention_text else None
                if entity.normalized_value and entity.normalized_value.money_value:
                    currency = entity.normalized_value.money_value.currency_code
            elif entity.type == "tax_amount":
                tax_amount = float(entity.mention_text) if entity.mention_text else None
            elif entity.type == "line_item":
                item_description = None
                item_quantity = None
                item_amount = None
                for prop in entity.properties:
                    if prop.type == "description":
                        item_description = prop.mention_text
                    elif prop.type == "quantity":
                        item_quantity = float(prop.mention_text) if prop.mention_text else None
                    elif prop.type == "amount":
                        item_amount = float(prop.mention_text) if prop.mention_text else None
                items.append(LineItem(description=item_description, quantity=item_quantity, amount=item_amount))

    extracted_receipt = ExtractedReceipt(
        merchant=merchant_name,
        tax=tax_amount,
        total=total_amount,
        currency=currency,
        items=items
    )

    return extracted_receipt.dict()
