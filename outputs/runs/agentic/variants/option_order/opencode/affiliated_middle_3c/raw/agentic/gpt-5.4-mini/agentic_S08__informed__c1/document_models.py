from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class FieldItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None


@dataclass
class DocumentExtractionRequest:
    document: Any
    locale: Optional[str] = None


@dataclass
class DocumentExtractionResponse:
    fields: Dict[str, Any] = field(default_factory=dict)
    confidence: Dict[str, float] = field(default_factory=dict)


def normalize_currency(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).replace(",", "").replace("$", "").strip()
    try:
        return float(text)
    except ValueError:
        return None


def normalize_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for item in items or []:
        normalized.append(
            {
                "description": item.get("description") or item.get("name"),
                "quantity": normalize_currency(item.get("quantity")),
                "unit_price": normalize_currency(
                    item.get("unit_price") or item.get("price")
                ),
                "amount": normalize_currency(item.get("amount") or item.get("total")),
            }
        )
    return normalized
