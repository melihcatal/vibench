from typing import Dict, Any, Optional
from datetime import datetime


def normalize_expense(
    extracted_data: Dict[str, Any], document_type: str
) -> Dict[str, Any]:
    normalized = {
        "document_type": document_type,
        "vendor_or_merchant": extracted_data.get("vendor")
        or extracted_data.get("merchant"),
        "date": _normalize_date(extracted_data.get("date")),
        "total_amount": float(extracted_data.get("total") or 0),
        "tax_amount": float(extracted_data.get("tax") or 0),
        "items": _normalize_items(
            extracted_data.get("line_items") or extracted_data.get("items")
        ),
        "confidence_score": float(extracted_data.get("confidence", 0)),
        "currency": extracted_data.get("currency", "USD"),
    }
    return normalized


def _normalize_date(date_str: Optional[str]) -> Optional[str]:
    if not date_str:
        return None
    try:
        date_obj = (
            datetime.fromisoformat(date_str) if isinstance(date_str, str) else date_str
        )
        return date_obj.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return None


def _normalize_items(items: Optional[list]) -> list:
    if not items:
        return []
    normalized_items = []
    for item in items:
        normalized_items.append(
            {
                "description": item.get("description", ""),
                "quantity": float(item.get("quantity", 1)),
                "unit_price": float(item.get("unit_price", 0)),
                "total_price": float(
                    item.get("total_price", 0) or item.get("total_amount", 0)
                ),
            }
        )
    return normalized_items
