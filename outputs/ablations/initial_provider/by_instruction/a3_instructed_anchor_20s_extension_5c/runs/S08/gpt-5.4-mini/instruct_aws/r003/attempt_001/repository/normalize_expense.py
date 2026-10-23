from typing import Any, Dict


def normalize_expense(fields: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "vendor": fields.get("vendor") or fields.get("merchant"),
        "date": fields.get("date"),
        "subtotal": fields.get("subtotal"),
        "tax": fields.get("tax"),
        "total": fields.get("total"),
        "currency": fields.get("currency", "USD"),
        "items": fields.get("line_items") or fields.get("items") or [],
        "confidence": fields.get("confidence", {}),
    }
