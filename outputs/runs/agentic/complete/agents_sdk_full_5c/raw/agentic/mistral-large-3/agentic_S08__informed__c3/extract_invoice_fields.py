import os
from typing import Dict, Any
from document_client import get_document_client
from document_models import InvoiceResponse


def extract_invoice_fields(file_path: str) -> InvoiceResponse:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Azure Document Intelligence.
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    model_id = "prebuilt-invoice"

    client = get_document_client("azure", endpoint=endpoint, key=key)

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(model_id=model_id, document=f)

    result = poller.result()

    invoice_data: Dict[str, Any] = {
        "vendor": result.get("vendor", {}).get("name", ""),
        "date": result.get("invoice_date", ""),
        "total": result.get("invoice_total", {}).get("amount", 0.0),
        "line_items": [],
        "confidence": result.get("confidence", 0.0),
    }

    for item in result.get("items", []):
        invoice_data["line_items"].append({
            "description": item.get("description", ""),
            "amount": item.get("amount", 0.0),
            "quantity": item.get("quantity", 0),
        })

    return InvoiceResponse(**invoice_data)