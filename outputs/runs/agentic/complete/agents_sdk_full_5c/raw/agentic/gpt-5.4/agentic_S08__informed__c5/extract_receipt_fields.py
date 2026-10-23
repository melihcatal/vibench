from __future__ import annotations

from typing import Any, Dict, List, Optional

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import get_document_intelligence_client, read_bytes
from document_models import ExtractedDocument, LineItem, coerce_float, normalize_date


def _field_value(document: Any, name: str) -> Any:
    field = document.fields.get(name) if getattr(document, "fields", None) else None
    return getattr(field, "value", None) if field else None


def _field_confidence(document: Any, name: str) -> Optional[float]:
    field = document.fields.get(name) if getattr(document, "fields", None) else None
    return float(field.confidence) if field and field.confidence is not None else None


def extract_receipt_fields(file_path: str) -> Dict[str, Any]:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-invoice",
        body=AnalyzeDocumentRequest(bytes_source=read_bytes(file_path)),
    )
    result = poller.result()
    document = result.documents[0]

    items: List[LineItem] = []
    for entry in _field_value(document, "Items") or []:
        values = getattr(entry, "value", {}) or {}
        items.append(
            LineItem(
                description=str(getattr(values.get("Description"), "value", "") or ""),
                quantity=coerce_float(getattr(values.get("Quantity"), "value", None)),
                unit_price=coerce_float(getattr(values.get("UnitPrice"), "value", None)),
                amount=coerce_float(getattr(values.get("Amount"), "value", None)),
                confidence=float(getattr(entry, "confidence", 0.0) or 0.0),
            )
        )

    extracted = ExtractedDocument(
        document_type="receipt",
        merchant=str(_field_value(document, "VendorName") or "") or None,
        invoice_date=normalize_date(str(_field_value(document, "InvoiceDate") or "") or None),
        total=coerce_float(_field_value(document, "InvoiceTotal")),
        tax=coerce_float(_field_value(document, "TotalTax")),
        currency=str(_field_value(document, "CurrencyCode") or "") or None,
        line_items=items,
        notes=str(_field_value(document, "CustomerName") or "") or None,
        confidence={
            "merchant": _field_confidence(document, "VendorName") or 0.0,
            "tax": _field_confidence(document, "TotalTax") or 0.0,
            "total": _field_confidence(document, "InvoiceTotal") or 0.0,
            "items": _field_confidence(document, "Items") or 0.0,
        },
        raw_provider_response=result.as_dict(),
    )
    payload = extracted.to_dict()
    payload["items"] = payload.pop("line_items")
    return payload
