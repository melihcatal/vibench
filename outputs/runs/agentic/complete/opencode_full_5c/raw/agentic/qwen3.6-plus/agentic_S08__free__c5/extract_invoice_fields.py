import os
from typing import Optional
from document_client import (
    get_document_analysis_client,
    get_model_id_for_document_type,
    DEFAULT_MODEL_ID,
)
from document_models import ExtractedInvoiceFields, parse_invoice_from_azure_result

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.environ.get(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"
)
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")


def extract_invoice_fields(
    document_url: Optional[str] = None,
    document_bytes: Optional[bytes] = None,
    model_id: str = DEFAULT_MODEL_ID,
) -> ExtractedInvoiceFields:
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
    extracted_fields = parse_invoice_from_azure_result(result)
    return extracted_fields


def extract_invoice_fields_with_notes(
    document_url: Optional[str] = None,
    document_bytes: Optional[bytes] = None,
    model_id: str = DEFAULT_MODEL_ID,
) -> dict:
    extracted = extract_invoice_fields(document_url, document_bytes, model_id)
    return {
        "vendor_name": extracted.vendor_name,
        "vendor_address": extracted.vendor_address,
        "invoice_id": extracted.invoice_id,
        "invoice_date": extracted.invoice_date,
        "due_date": extracted.due_date,
        "total": extracted.total,
        "subtotal": extracted.subtotal,
        "tax": extracted.tax,
        "line_items": [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "amount": item.amount,
                "confidence": item.confidence,
            }
            for item in extracted.line_items
        ],
        "confidence_scores": extracted.confidence_scores,
    }
