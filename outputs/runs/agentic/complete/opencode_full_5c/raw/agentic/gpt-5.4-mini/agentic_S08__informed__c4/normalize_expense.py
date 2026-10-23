from datetime import date
from typing import Any, Dict

from document_models import StructuredDocumentResponse, normalize_field_map


STANDARD_SCHEMA = {"vendor": None, "date": None, "total": None, "tax": None, "currency": None, "line_items": []}


def normalize_expense(response: StructuredDocumentResponse) -> Dict[str, Any]:
    fields = normalize_field_map(response.fields)
    normalized = dict(STANDARD_SCHEMA)
    normalized["vendor"] = fields.get("VendorName", {}).get("value") or fields.get("MerchantName", {}).get("value")
    normalized["date"] = fields.get("InvoiceDate", {}).get("value")
    normalized["total"] = fields.get("InvoiceTotal", {}).get("value") or fields.get("Total", {}).get("value")
    normalized["tax"] = fields.get("TotalTax", {}).get("value")
    normalized["line_items"] = fields.get("Items", {}).get("value") or []
    normalized["source_provider"] = response.provider
    return normalized
