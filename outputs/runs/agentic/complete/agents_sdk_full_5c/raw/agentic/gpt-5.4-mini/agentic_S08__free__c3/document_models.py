from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional


@dataclass
class ConfidenceField:
    value: Any
    confidence: float = 0.0


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None


@dataclass
class ExtractedDocument:
    vendor: Optional[ConfidenceField] = None
    merchant: Optional[ConfidenceField] = None
    date: Optional[ConfidenceField] = None
    total: Optional[ConfidenceField] = None
    tax: Optional[ConfidenceField] = None
    notes: Optional[ConfidenceField] = None
    items: List[LineItem] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExpenseRecord:
    source_type: str
    vendor: str
    transaction_date: Optional[date]
    total: float
    tax: Optional[float]
    currency: str = "USD"
    items: List[Dict[str, Any]] = field(default_factory=list)


def normalize_amount(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = str(value).replace("$", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None
