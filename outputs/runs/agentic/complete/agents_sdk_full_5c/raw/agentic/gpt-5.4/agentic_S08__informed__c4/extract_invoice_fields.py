from __future__ import annotations

from typing import Any, Dict, List

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import field_confidence, field_content, get_document_intelligence_client, model_result_to_dict, read_bytes
from document_models import ExtractedDocument, LineItem, iso_date, safe_float


MODEL_ID = "prebuilt-invoice"
PROVIDER = "azure-document-intelligence"


def _parse_line_items(items_field: Any) -> List[LineItem]:
    parsed: List[LineItem] = []
    if not items_field or not getattr(items_field, "value_array", None):
        return parsed
    for entry in items_field.value_array:
        values = getattr(entry, "value_object", {}) or {}
        parsed.append(
            LineItem(
                description=str(field_content(values.get("Description")) or ""),
                quantity=safe_float(field_content(values.get("Quantity"))),
                unit_price=safe_float(field_content(values.get("UnitPrice"))),
                amount=safe_float(field_content(values.get("Amount"))),
                confidence=field_confidence(entry),
            )
        )
    return parsed


def extract_invoice_fields(file_path: str) -> Dict[str, Any]:
    client = get_document_intelligence_client()
    with open(file_path, "rb") as handle:
        poller = client.begin_analyze_document(
            model_id=MODEL_ID,
            analyze_request=AnalyzeDocumentRequest(bytes_source=handle.read()),
        )
    result = poller.result()
    doc = result.documents[0] if getattr(result, "documents", None) else None
    fields = getattr(doc, "fields", {}) if doc else {}

    extracted = ExtractedDocument(
        document_type="invoice",
        vendor=str(field_content(fields.get("VendorName")) or "") or None,
        invoice_date=iso_date(field_content(fields.get("InvoiceDate"))),
        total=safe_float(field_content(fields.get("InvoiceTotal"))),
        currency=getattr(getattr(fields.get("InvoiceTotal"), "value_currency", None), "currency_symbol", None),
        line_items=_parse_line_items(fields.get("Items")),
        raw_fields=model_result_to_dict(result),
        provider=PROVIDER,
        source_confidence={
            "vendor": field_confidence(fields.get("VendorName")) or 0.0,
            "date": field_confidence(fields.get("InvoiceDate")) or 0.0,
            "total": field_confidence(fields.get("InvoiceTotal")) or 0.0,
            "items": field_confidence(fields.get("Items")) or 0.0,
        },
        notes=str(field_content(fields.get("CustomerAddressRecipient")) or "") or None,
    )
    return extracted.to_dict()
