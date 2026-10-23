import os
from typing import Any, Dict

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import build_document_intelligence_client, load_service_config
from document_models import InvoiceExtractionRequest, normalize_money, normalize_text


def extract_invoice_fields(request: InvoiceExtractionRequest) -> Dict[str, Any]:
    config = load_service_config()
    client = build_document_intelligence_client(config)
    poller = client.begin_analyze_document(
        "prebuilt-invoice",
        body=request.content,
        content_type=request.content_type,
    )
    result = poller.result()
    fields = result.documents[0].fields if getattr(result, "documents", None) else {}
    vendor = normalize_text(fields.get("VendorName").value if fields.get("VendorName") else None)
    date = normalize_text(fields.get("InvoiceDate").value if fields.get("InvoiceDate") else None)
    total = normalize_money(fields.get("InvoiceTotal").value if fields.get("InvoiceTotal") else None)
    items = []
    for item in (fields.get("Items").value if fields.get("Items") else []) or []:
        items.append({
            "description": normalize_text(item.get("Description").value if item.get("Description") else None),
            "quantity": item.get("Quantity").value if item.get("Quantity") else None,
            "amount": normalize_money(item.get("Amount").value if item.get("Amount") else None),
        })
    return {"vendor": vendor, "date": date, "total": total, "line_items": items}
