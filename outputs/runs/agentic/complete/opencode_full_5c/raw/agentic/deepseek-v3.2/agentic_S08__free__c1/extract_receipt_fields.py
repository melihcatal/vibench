import os
from typing import Dict, List, Any
import json
from document_client import get_document_client
from document_models import ReceiptExtractionRequest, ReceiptExtractionResponse


def extract_receipt_fields(receipt_image_path: str) -> Dict[str, Any]:
    """
    Extract merchant, tax, total, and items from a receipt using Google Document AI.
    """
    client = get_document_client()

    with open(receipt_image_path, "rb") as f:
        receipt_bytes = f.read()

    request = ReceiptExtractionRequest(
        document_bytes=receipt_bytes, document_type="receipt"
    )

    # Use Google Document AI
    from google.cloud import documentai
    from google.api_core.client_options import ClientOptions

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")

    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    docai_client = documentai.DocumentProcessorServiceClient(
        client_options=client_options
    )

    processor_name = docai_client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=receipt_bytes, mime_type="image/jpeg")

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    result = docai_client.process_document(request=request)
    document = result.document

    extracted_fields = {}

    # Extract merchant information
    merchant_name = None
    merchant_address = None
    merchant_phone = None

    for entity in document.entities:
        if entity.type_ == "merchant_name" and entity.mention_text:
            merchant_name = entity.mention_text
        elif entity.type_ == "merchant_address" and entity.mention_text:
            merchant_address = entity.mention_text
        elif entity.type_ == "merchant_phone" and entity.mention_text:
            merchant_phone = entity.mention_text

    # Extract tax
    tax_amount = None
    tax_rate = None

    for entity in document.entities:
        if entity.type_ == "tax" and entity.normalized_value:
            tax_amount = float(entity.normalized_value.text)
        elif entity.type_ == "tax_rate" and entity.normalized_value:
            tax_rate = float(entity.normalized_value.text.replace("%", ""))

    # Extract total
    total_amount = None
    for entity in document.entities:
        if entity.type_ == "total_amount" and entity.normalized_value:
            total_amount = float(entity.normalized_value.text)

    # Extract items
    items = []
    current_item = {}

    for entity in document.entities:
        if entity.type_ == "line_item/description" and entity.mention_text:
            if current_item:
                items.append(current_item)
                current_item = {}
            current_item["description"] = entity.mention_text
        elif entity.type_ == "line_item/quantity" and entity.normalized_value:
            current_item["quantity"] = float(entity.normalized_value.text)
        elif entity.type_ == "line_item/unit_price" and entity.normalized_value:
            current_item["unit_price"] = float(entity.normalized_value.text)
        elif entity.type_ == "line_item/amount" and entity.normalized_value:
            current_item["amount"] = float(entity.normalized_value.text)

    if current_item:
        items.append(current_item)

    # Extract date
    transaction_date = None
    for entity in document.entities:
        if entity.type_ == "transaction_date" and entity.normalized_value:
            transaction_date = entity.normalized_value.text

    extracted_fields = {
        "merchant": {
            "name": merchant_name,
            "address": merchant_address,
            "phone": merchant_phone,
        },
        "tax": {"amount": tax_amount, "rate": tax_rate},
        "total": total_amount,
        "items": items,
        "date": transaction_date,
        "confidence": document.confidence,
        "provider": "google_document_ai",
        "model": "us_receipt_processor",
    }

    return extracted_fields
