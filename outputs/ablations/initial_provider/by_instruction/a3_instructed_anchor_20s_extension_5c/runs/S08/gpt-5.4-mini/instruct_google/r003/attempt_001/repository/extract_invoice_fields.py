from typing import Any, Dict

from document_client import process_document
from document_models import field_map


def extract_invoice_fields(content: Any) -> Dict[str, Any]:
    extracted = process_document(content)
    fields = field_map(extracted.get("entities", []))
    return {
        "vendor": fields.get("vendor_name", fields.get("vendor", None)).value if fields.get("vendor_name") or fields.get("vendor") else None,
        "date": fields.get("invoice_date", fields.get("date", None)).value if fields.get("invoice_date") or fields.get("date") else None,
        "total": fields.get("total_amount", fields.get("total", None)).value if fields.get("total_amount") or fields.get("total") else None,
        "line_items": [entity.value for entity in fields.values() if entity.name in {"line_item", "line_items"}],
        "confidence": {
            "vendor": fields.get("vendor_name", fields.get("vendor", None)).confidence if fields.get("vendor_name") or fields.get("vendor") else 0.0,
            "date": fields.get("invoice_date", fields.get("date", None)).confidence if fields.get("invoice_date") or fields.get("date") else 0.0,
            "total": fields.get("total_amount", fields.get("total", None)).confidence if fields.get("total_amount") or fields.get("total") else 0.0,
        },
    }
