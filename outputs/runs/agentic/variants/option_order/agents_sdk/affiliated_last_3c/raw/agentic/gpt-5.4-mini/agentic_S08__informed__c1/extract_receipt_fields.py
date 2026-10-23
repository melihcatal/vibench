from __future__ import annotations

from typing import Any, Dict

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import DEFAULT_RECEIPT_MODEL_ID, build_document_intelligence_client, load_document_client_config
from document_models import ExtractedDocumentResponse, LineItem, StructuredDocumentRequest

PROVIDER_NAME = "azure-ai-documentintelligence"
MODEL_ID = "prebuilt-receipt"


def extract_receipt_fields(request: StructuredDocumentRequest) -> ExtractedDocumentResponse:
    config = load_document_client_config(DEFAULT_RECEIPT_MODEL_ID)
    client = build_document_intelligence_client(config)
    poller = client.begin_analyze_document(
        model_id=MODEL_ID,
        analyze_request=AnalyzeDocumentRequest(bytes_source=request.document_bytes),
        content_type=request.content_type,
    )
    result = poller.result()
    document = result.documents[0] if result.documents else None
    fields: Dict[str, Any] = {}
    items = []
    if document and document.fields:
        fields = {
            "merchant": getattr(document.fields.get("MerchantName"), "content", None),
            "tax": getattr(document.fields.get("TotalTax"), "value", None),
            "total": getattr(document.fields.get("Total"), "value", None),
        }
        for item in (document.fields.get("Items") or []).value or []:
            items.append(
                LineItem(
                    description=getattr(item.value.get("Description"), "content", ""),
                    quantity=getattr(item.value.get("Quantity"), "value", None),
                    unit_price=getattr(item.value.get("Price"), "value", None),
                    amount=getattr(item.value.get("TotalPrice"), "value", None),
                    confidence=getattr(item, "confidence", None),
                )
            )
    return ExtractedDocumentResponse(provider=PROVIDER_NAME, fields=fields, line_items=items, raw={"result": result.to_dict() if hasattr(result, "to_dict") else {}})
