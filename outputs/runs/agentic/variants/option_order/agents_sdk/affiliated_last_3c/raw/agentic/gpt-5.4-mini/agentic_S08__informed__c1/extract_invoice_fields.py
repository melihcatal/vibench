from __future__ import annotations

from typing import Any, Dict

from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest

from document_client import DEFAULT_INVOICE_MODEL_ID, build_document_intelligence_client, load_document_client_config
from document_models import ExtractedDocumentResponse, LineItem, StructuredDocumentRequest

PROVIDER_NAME = "azure-ai-documentintelligence"
MODEL_ID = "prebuilt-invoice"


def extract_invoice_fields(request: StructuredDocumentRequest) -> ExtractedDocumentResponse:
    config = load_document_client_config(DEFAULT_INVOICE_MODEL_ID)
    client = build_document_intelligence_client(config)
    poller = client.begin_analyze_document(
        model_id=MODEL_ID,
        analyze_request=AnalyzeDocumentRequest(bytes_source=request.document_bytes),
        content_type=request.content_type,
    )
    result: AnalyzeResult = poller.result()
    document = result.documents[0] if result.documents else None
    fields: Dict[str, Any] = {}
    line_items = []
    if document and document.fields:
        vendor_field = document.fields.get("VendorName") or document.fields.get("MerchantName")
        date_field = document.fields.get("InvoiceDate") or document.fields.get("TransactionDate")
        total_field = document.fields.get("InvoiceTotal") or document.fields.get("Total")
        fields = {
            "vendor": getattr(vendor_field, "content", None),
            "date": getattr(date_field, "content", None),
            "total": getattr(total_field, "content", None),
        }
        for item in (document.fields.get("Items") or []).value or []:
            line_items.append(
                LineItem(
                    description=getattr(item.value.get("Description"), "content", ""),
                    quantity=getattr(item.value.get("Quantity"), "value", None),
                    unit_price=getattr(item.value.get("UnitPrice"), "value", None),
                    amount=getattr(item.value.get("Amount"), "value", None),
                    confidence=getattr(item, "confidence", None),
                )
            )
    return ExtractedDocumentResponse(provider=PROVIDER_NAME, fields=fields, line_items=line_items, raw={"result": result.to_dict() if hasattr(result, "to_dict") else {}})
