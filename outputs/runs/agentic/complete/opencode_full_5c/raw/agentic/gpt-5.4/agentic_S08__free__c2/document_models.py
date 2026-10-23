from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class DocumentSource:
    content_base64: str
    mime_type: str
    file_name: Optional[str] = None


@dataclass
class ConfidenceValue:
    value: Any
    confidence: float


@dataclass
class LineItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: float = 0.0


@dataclass
class ExtractedInvoice:
    vendor: Optional[ConfidenceValue] = None
    invoice_date: Optional[ConfidenceValue] = None
    total: Optional[ConfidenceValue] = None
    line_items: List[LineItem] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractedReceipt:
    merchant: Optional[ConfidenceValue] = None
    tax: Optional[ConfidenceValue] = None
    total: Optional[ConfidenceValue] = None
    items: List[LineItem] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationIssue:
    field: str
    message: str


@dataclass
class ValidationResult:
    valid: bool
    issues: List[ValidationIssue]


def model_to_dict(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    if isinstance(value, list):
        return [model_to_dict(item) for item in value]
    if isinstance(value, dict):
        return {k: model_to_dict(v) for k, v in value.items()}
    return value


def to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def make_confidence_value(value: Any, confidence: Any) -> Optional[ConfidenceValue]:
    if value in (None, ""):
        return None
    score = to_float(confidence)
    return ConfidenceValue(value=value, confidence=score if score is not None else 0.0)


def normalize_line_item(payload: Dict[str, Any]) -> LineItem:
    return LineItem(
        description=payload.get("description")
        or payload.get("name")
        or payload.get("text"),
        quantity=to_float(payload.get("quantity")),
        unit_price=to_float(payload.get("unit_price") or payload.get("price")),
        amount=to_float(payload.get("amount") or payload.get("total")),
        confidence=to_float(payload.get("confidence")) or 0.0,
    )


def normalized_expense_schema(
    kind: str,
    source_id: Optional[str],
    currency: Optional[str],
    vendor: Optional[str],
    date: Optional[str],
    total: Optional[float],
    tax: Optional[float],
    items: List[LineItem],
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload = {
        "document_type": kind,
        "source_id": source_id,
        "currency": currency,
        "vendor": vendor,
        "date": date,
        "total": total,
        "tax": tax,
        "items": [model_to_dict(item) for item in items],
    }
    if extra:
        payload.update(extra)
    return payload
