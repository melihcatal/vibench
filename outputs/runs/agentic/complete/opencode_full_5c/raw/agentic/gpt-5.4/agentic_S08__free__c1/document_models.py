from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentSource:
    content_base64: Optional[str] = None
    mime_type: Optional[str] = None
    gcs_uri: Optional[str] = None

    def to_google_document(self) -> Dict[str, Any]:
        if self.gcs_uri:
            return {"gcs_content_uri": self.gcs_uri, "mime_type": self.mime_type}
        payload: Dict[str, Any] = {"mime_type": self.mime_type}
        if self.content_base64:
            payload["content"] = self.content_base64
        return payload


@dataclass
class ExtractedField:
    name: str
    value: Any
    confidence: float = 0.0
    normalized_value: Any = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "confidence": self.confidence,
            "normalized_value": self.normalized_value,
        }


@dataclass
class LineItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "amount": self.amount,
            "confidence": self.confidence,
        }


@dataclass
class ExtractionResult:
    document_type: str
    provider: str
    fields: Dict[str, ExtractedField] = field(default_factory=dict)
    line_items: List[LineItem] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_type": self.document_type,
            "provider": self.provider,
            "fields": {key: value.to_dict() for key, value in self.fields.items()},
            "line_items": [item.to_dict() for item in self.line_items],
            "raw_response": self.raw_response,
        }


def normalize_currency(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = value.replace("$", "").replace(",", "").strip()
        if not cleaned:
            return None
        return float(cleaned)
    return None


def normalize_confidence(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return max(0.0, min(float(value), 1.0))
    return 0.0


def to_standard_expense_schema(extraction: Dict[str, Any]) -> Dict[str, Any]:
    fields = extraction.get("fields", {})
    return {
        "document_type": extraction.get("document_type"),
        "provider": extraction.get("provider"),
        "merchant_name": _field_value(fields, "vendor")
        or _field_value(fields, "merchant"),
        "transaction_date": _field_value(fields, "date"),
        "tax_amount": normalize_currency(_field_value(fields, "tax")),
        "total_amount": normalize_currency(_field_value(fields, "total")),
        "currency": _field_value(fields, "currency") or "USD",
        "items": extraction.get("line_items", []),
        "notes": _field_value(fields, "notes") or _field_value(fields, "memo"),
    }


def _field_value(fields: Dict[str, Any], key: str) -> Any:
    field_value = fields.get(key)
    if isinstance(field_value, dict):
        return field_value.get("normalized_value") or field_value.get("value")
    return None
