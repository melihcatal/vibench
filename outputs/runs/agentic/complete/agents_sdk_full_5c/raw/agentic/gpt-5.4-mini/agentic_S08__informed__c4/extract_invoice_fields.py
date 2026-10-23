from __future__ import annotations

from typing import Any, Dict, List

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import get_document_intelligence_client, field_value
from document_models import LineItem, StructuredDocumentExtractionRequest, StructuredDocumentExtractionResponse

MODEL_ID = "prebuilt-invoice"


def extract_invoice_fields(request: StructuredDocumentExtractionRequest) -> StructuredDocumentExtractionResponse:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        MODEL_ID,
        AnalyzeDocumentRequest(bytes_source=request.content),
        content_type=request.content_type,
    )
    result = poller.result()
    doc = result.documents[0] if getattr(result, "documents", None) else None
    fields = getattr(doc, "fields", {}) if doc else {}

    line_items: List[LineItem] = []
    for item in field_value(fields.get("Items")) or []:
        item_fields = getattr(item, "value", item)
        if isinstance(item_fields, dict):
            line_items.append(
                LineItem(
                    description=str(field_value(item_fields.get("Description")) or ""),
                    quantity=_as_float(field_value(item_fields.get("Quantity"))),
                    unit_price=_as_float(field_value(item_fields.get("UnitPrice"))),
                    amount=_as_float(field_value(item_fields.get("Amount"))),
                )
            )

    return StructuredDocumentExtractionResponse(
        vendor=str(field_value(fields.get("VendorName")) or ""),
        date=str(field_value(fields.get("InvoiceDate")) or ""),
        total=_as_float(field_value(fields.get("InvoiceTotal"))),
        line_items=line_items,
        confidence=_as_float(getattr(doc, "confidence", None)),
        raw=result.to_dict() if hasattr(result, "to_dict") else None,
    )


def _as_float(value: Any) -> Any:
    try:
        return float(value) if value is not None and value != "" else None
    except (TypeError, ValueError):
        return None
