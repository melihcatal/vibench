import os
from google.cloud import documentai_v1 as documentai
from document_client import get_document_ai_client, get_document_ai_processor_path
from document_models import LineItem

def extract_receipt_fields(payload, config=None):
    config = config or {}
    project_id = config.get("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"))
    location = config.get("location", "us")  # e.g., "us"
    processor_id = config.get("processor_id", os.environ.get("DOCUMENT_AI_RECEIPT_PROCESSOR_ID"))

    if not all([project_id, location, processor_id]):
        raise ValueError("Google Cloud project_id, location, and Document AI receipt processor_id must be provided.")

    client = get_document_ai_client()
    processor_path = get_document_ai_processor_path(project_id, location, processor_id)

    document_bytes = payload["document_bytes"]
    raw_document = documentai.RawDocument(
        content=document_bytes,
        mime_type="application/pdf" # Assuming PDF for receipts, adjust as needed
    )

    request = documentai.ProcessRequest(name=processor_path, raw_document=raw_document)
    response = client.process_document(request=request)
    document = response.document

    merchant_name = ""
    transaction_date = ""
    total_amount = ""
    tax_amount = ""
    currency = ""
    items = []

    for entity in document.entities:
        if entity.type == "merchant_name":
            merchant_name = entity.mention_text
        elif entity.type == "transaction_date":
            transaction_date = entity.mention_text
        elif entity.type == "total_amount":
            total_amount = entity.mention_text
            if entity.normalized_value and entity.normalized_value.money_value:
                currency = entity.normalized_value.money_value.currency_code
        elif entity.type == "tax_amount":
            tax_amount = entity.mention_text
        elif entity.type == "line_item":
            item_description = ""
            item_quantity = ""
            item_amount = ""
            for prop in entity.properties:
                if prop.type == "description":
                    item_description = prop.mention_text
                elif prop.type == "quantity":
                    item_quantity = prop.mention_text
                elif prop.type == "amount":
                    item_amount = prop.mention_text
            items.append(LineItem(description=item_description, quantity=item_quantity, amount=item_amount))

    return {
        "merchant": merchant_name,
        "date": transaction_date,
        "total": total_amount,
        "tax": tax_amount,
        "currency": currency,
        "items": [item.dict() for item in items],
        "raw_document_ai_response": document.to_dict()
    }
