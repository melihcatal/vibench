from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentField:
    value: Any
    confidence: float = 0.0


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: float = 0.0


@dataclass
class DocumentExtractionResult:
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    currency: Optional[str] = None
    notes: Optional[str] = None
    items: List[LineItem] = field(default_factory=list)
    confidence: float = 0.0


def standardize_expense_record(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "vendor": data.get("vendor") or data.get("merchant"),
        "date": data.get("date"),
        "total": data.get("total"),
        "tax": data.get("tax"),
        "currency": data.get("currency"),
        "items": data.get("items", []),
        "notes": data.get("notes"),
        "confidence": float(data.get("confidence", 0.0) or 0.0),
    }
