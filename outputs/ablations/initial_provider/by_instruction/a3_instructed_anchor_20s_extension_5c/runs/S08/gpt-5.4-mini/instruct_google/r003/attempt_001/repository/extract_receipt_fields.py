from typing import Any, Dict

from document_client import process_document
from document_models import field_map


def extract_receipt_fields(content: Any) -> Dict[str, Any]:
    extracted = process_document(content)
    fields = field_map(extracted.get("entities", []))
    return {
        "merchant": fields.get("merchant_name", fields.get("merchant", None)).value if fields.get("merchant_name") or fields.get("merchant") else None,
        "tax": fields.get("tax_amount", fields.get("tax", None)).value if fields.get("tax_amount") or fields.get("tax") else None,
        "total": fields.get("total_amount", fields.get("total", None)).value if fields.get("total_amount") or fields.get("total") else None,
        "items": [entity.value for entity in fields.values() if entity.name in {"item", "items"}],
    }
