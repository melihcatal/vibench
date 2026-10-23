from google.cloud import documentai_v1 as documentai
import os
from typing import Dict, Any, List
from document_models import ExtractedDocument, LineItem
from document_client import load_config, get_google_document_ai_client

def extract_receipt_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    config = load_config()
    project_id = config.get("google_project_id")
    location = config.get("google_location")
    processor_id = config.get("google_document_ai_processor_id_receipt")

    if not all([project_id, location, processor_id]):
        raise ValueError("Google Cloud project ID, location, or Document AI processor ID for receipts is not configured.")

    client = get_google_document_ai_client()

    name = client.processor_path(project_id, location, processor_id)

    document_bytes = payload["document_bytes"]
    mime_type = payload.get("mime_type", "application/pdf")

    raw_document = documentai.RawDocument(
        content=document_bytes,
        mime_type=mime_type,
    )

    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
    )

    result = client.process_document(request=request)
    document = result.document

    merchant_name = ""
    total_amount = ""
    tax_amount = ""
    transaction_date = ""
    items: List[LineItem] = []

    for entity in document.entities:
        if entity.type == "merchant_name":
            merchant_name = entity.mention_text
        elif entity.type == "total_amount":
            total_amount = entity.mention_text
        elif entity.type == "tax_amount":
            tax_amount = entity.mention_text
        elif entity.type == "transaction_date":
            transaction_date = entity.mention_text
        elif entity.type == "line_item":
            description = ""
            quantity = ""
            amount = ""
            for prop in entity.properties:
                if prop.type == "description":
                    description = prop.mention_text
                elif prop.type == "quantity":
                    quantity = prop.mention_text
                elif prop.type == "amount":
                    amount = prop.mention_text
            items.append(LineItem(description=description, quantity=quantity, amount=amount))

    extracted_receipt = ExtractedDocument(
        merchant=merchant_name,
        date=transaction_date,
        total=total_amount,
        tax=tax_amount,
        items=items,
    )

    return {"receipt": extracted_receipt.dict()}
