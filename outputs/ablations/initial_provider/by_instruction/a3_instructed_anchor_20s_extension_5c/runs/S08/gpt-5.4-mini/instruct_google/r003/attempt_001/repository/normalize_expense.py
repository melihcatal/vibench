from typing import Any, Dict


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "party": extracted.get("vendor") or extracted.get("merchant"),
        "date": extracted.get("date"),
        "amount": extracted.get("total"),
        "tax": extracted.get("tax"),
        "items": extracted.get("line_items") or extracted.get("items") or [],
        "confidence": extracted.get("confidence", {}),
        "source": "google_document_ai",
    }
