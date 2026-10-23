from typing import Any, Dict

from document_models import normalize_money, normalize_text


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "merchant": normalize_text(extracted.get("merchant") or extracted.get("vendor")),
        "date": normalize_text(extracted.get("date")),
        "total": normalize_money(extracted.get("total")),
        "tax": normalize_money(extracted.get("tax")),
        "items": extracted.get("items") or extracted.get("line_items") or [],
    }
