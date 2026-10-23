from typing import Any, Dict

from azure.ai.documentintelligence import DocumentIntelligenceClient

from document_client import build_document_intelligence_client, load_service_config
from document_models import ReceiptExtractionRequest, normalize_money, normalize_text


def extract_receipt_fields(request: ReceiptExtractionRequest) -> Dict[str, Any]:
    config = load_service_config()
    client = build_document_intelligence_client(config)
    poller = client.begin_analyze_document("prebuilt-receipt", body=request.content, content_type=request.content_type)
    result = poller.result()
    fields = result.documents[0].fields if getattr(result, "documents", None) else {}
    merchant = normalize_text(fields.get("MerchantName").value if fields.get("MerchantName") else None)
    tax = normalize_money(fields.get("TotalTax").value if fields.get("TotalTax") else None)
    total = normalize_money(fields.get("Total").value if fields.get("Total") else None)
    items = []
    for item in (fields.get("Items").value if fields.get("Items") else []) or []:
        items.append({"name": normalize_text(item.get("Name").value if item.get("Name") else None), "price": normalize_money(item.get("TotalPrice").value if item.get("TotalPrice") else None)})
    return {"merchant": merchant, "tax": tax, "total": total, "items": items}
