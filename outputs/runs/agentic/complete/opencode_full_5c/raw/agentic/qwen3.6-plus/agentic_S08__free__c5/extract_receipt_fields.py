import os
from typing import Optional
from document_client import get_document_analysis_client, RECEIPT_MODEL_ID
from document_models import ExtractedReceiptFields, parse_receipt_from_azure_result

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.environ.get(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"
)
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")


def extract_receipt_fields(
    document_url: Optional[str] = None,
    document_bytes: Optional[bytes] = None,
    model_id: str = RECEIPT_MODEL_ID,
) -> ExtractedReceiptFields:
    client = get_document_analysis_client(model_id)

    if document_url:
        poller = client.begin_analyze_document_from_url(
            model_id=model_id, document_url=document_url
        )
    elif document_bytes:
        poller = client.begin_analyze_document(
            model_id=model_id, document=document_bytes
        )
    else:
        raise ValueError("Either document_url or document_bytes must be provided")

    result = poller.result()
    extracted_fields = parse_receipt_from_azure_result(result)
    return extracted_fields


def extract_receipt_fields_with_items(
    document_url: Optional[str] = None,
    document_bytes: Optional[bytes] = None,
    model_id: str = RECEIPT_MODEL_ID,
) -> dict:
    extracted = extract_receipt_fields(document_url, document_bytes, model_id)
    return {
        "merchant_name": extracted.merchant_name,
        "merchant_address": extracted.merchant_address,
        "transaction_date": extracted.transaction_date,
        "transaction_time": extracted.transaction_time,
        "total": extracted.total,
        "subtotal": extracted.subtotal,
        "tax": extracted.tax,
        "items": [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "amount": item.amount,
                "confidence": item.confidence,
            }
            for item in extracted.items
        ],
        "confidence_scores": extracted.confidence_scores,
    }
