from __future__ import annotations

from dataclasses import asdict, dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional


def _to_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(Decimal(str(value)))
    except (InvalidOperation, ValueError, TypeError):
        return None


def _to_confidence(value: Any) -> float:
    numeric = _to_float(value)
    if numeric is None:
        return 0.0
    return max(0.0, min(1.0, numeric))


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "quantity": _to_float(self.quantity),
            "unit_price": _to_float(self.unit_price),
            "amount": _to_float(self.amount),
            "confidence": _to_confidence(self.confidence),
        }


@dataclass
class ExtractionResult:
    document_type: str
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    invoice_date: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    currency: Optional[str] = None
    notes: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["total"] = _to_float(self.total)
        payload["tax"] = _to_float(self.tax)
        payload["line_items"] = [item.to_dict() for item in self.line_items]
        payload["confidence_scores"] = {
            key: _to_confidence(value) for key, value in self.confidence_scores.items()
        }
        return payload


@dataclass
class ValidationResult:
    valid: bool
    missing_fields: List[str] = field(default_factory=list)
    low_confidence_fields: List[str] = field(default_factory=list)
    normalized: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def build_line_item(source: Dict[str, Any]) -> LineItem:
    return LineItem(
        description=str(source.get("description") or source.get("name") or "").strip(),
        quantity=_to_float(source.get("quantity")),
        unit_price=_to_float(source.get("unit_price") or source.get("price")),
        amount=_to_float(source.get("amount") or source.get("total")),
        confidence=_to_confidence(source.get("confidence") or source.get("score")),
    )


def compact_dict(payload: Dict[str, Any]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for key, value in payload.items():
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        if isinstance(value, list):
            filtered = [item for item in value if item not in (None, "", {}, [])]
            if filtered:
                result[key] = filtered
            continue
        result[key] = value
    return result


def standard_expense_schema(extraction: ExtractionResult) -> Dict[str, Any]:
    party_name = extraction.vendor or extraction.merchant
    schema = {
        "document_type": extraction.document_type,
        "party": {"name": party_name},
        "document_date": extraction.invoice_date,
        "totals": {
            "subtotal": None,
            "tax": _to_float(extraction.tax),
            "grand_total": _to_float(extraction.total),
            "currency": extraction.currency or "USD",
        },
        "items": [item.to_dict() for item in extraction.line_items],
        "notes": extraction.notes,
        "confidence": extraction.confidence_scores,
        "source": extraction.raw_response,
    }
    return compact_dict(schema)
