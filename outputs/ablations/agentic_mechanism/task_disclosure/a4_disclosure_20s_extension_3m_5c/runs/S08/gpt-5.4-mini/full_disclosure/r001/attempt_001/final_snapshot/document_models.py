from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Mapping, MutableMapping, Optional


def _coerce_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip().replace(",", "")
        if not text:
            return None
        try:
            return float(text)
        except ValueError:
            return None
    return None


def _coerce_int(value: Any) -> Optional[int]:
    num = _coerce_float(value)
    return int(num) if num is not None else None


def _coerce_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _coerce_mapping(value: Any) -> Dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


@dataclass
class FieldValue:
    value: Any = None
    confidence: Optional[float] = None
    raw_text: Optional[str] = None

    @classmethod
    def from_any(cls, value: Any) -> "FieldValue":
        if isinstance(value, cls):
            return value
        if isinstance(value, Mapping):
            return cls(
                value=value.get("value"),
                confidence=_coerce_float(value.get("confidence")),
                raw_text=_coerce_str(value.get("raw_text") or value.get("text")),
            )
        return cls(value=value)

    def to_dict(self) -> Dict[str, Any]:
        data = {"value": self.value, "confidence": self.confidence, "raw_text": self.raw_text}
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class DocumentRequest:
    document_id: Optional[str] = None
    mime_type: Optional[str] = None
    filename: Optional[str] = None
    text: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "DocumentRequest":
        return cls(
            document_id=_coerce_str(payload.get("document_id") or payload.get("id")),
            mime_type=_coerce_str(payload.get("mime_type") or payload.get("content_type")),
            filename=_coerce_str(payload.get("filename") or payload.get("name")),
            text=_coerce_str(payload.get("text") or payload.get("content")),
            metadata=_coerce_mapping(payload.get("metadata")),
        )

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return {k: v for k, v in data.items() if v not in (None, {}, [])}


@dataclass
class DocumentField:
    name: str
    value: Any = None
    confidence: Optional[float] = None
    source_text: Optional[str] = None

    @classmethod
    def from_any(cls, name: str, value: Any) -> "DocumentField":
        fv = FieldValue.from_any(value)
        return cls(name=name, value=fv.value, confidence=fv.confidence, source_text=fv.raw_text)

    def to_dict(self) -> Dict[str, Any]:
        data = {"name": self.name, "value": self.value, "confidence": self.confidence, "source_text": self.source_text}
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class DocumentResponse:
    provider: Optional[str] = None
    model: Optional[str] = None
    fields: Dict[str, DocumentField] = field(default_factory=dict)
    text: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "DocumentResponse":
        raw_fields = payload.get("fields") or {}
        fields: Dict[str, DocumentField] = {}
        if isinstance(raw_fields, Mapping):
            for key, value in raw_fields.items():
                fields[str(key)] = DocumentField.from_any(str(key), value)
        return cls(
            provider=_coerce_str(payload.get("provider")),
            model=_coerce_str(payload.get("model")),
            fields=fields,
            text=_coerce_str(payload.get("text") or payload.get("output_text")),
            metadata=_coerce_mapping(payload.get("metadata")),
        )

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "provider": self.provider,
            "model": self.model,
            "fields": {name: field.to_dict() for name, field in self.fields.items()},
            "text": self.text,
            "metadata": self.metadata,
        }
        return {k: v for k, v in data.items() if v not in (None, {}, [])}


@dataclass
class NormalizedItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "NormalizedItem":
        return cls(
            description=_coerce_str(payload.get("description") or payload.get("name") or payload.get("title")),
            quantity=_coerce_float(payload.get("quantity")),
            unit_price=_coerce_float(payload.get("unit_price") or payload.get("price")),
            amount=_coerce_float(payload.get("amount") or payload.get("total")),
        )

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class NormalizedExpense:
    provider: Optional[str] = None
    model: Optional[str] = None
    currency: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[str] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    tip: Optional[float] = None
    total: Optional[float] = None
    notes: Optional[str] = None
    items: list[NormalizedItem] = field(default_factory=list)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "NormalizedExpense":
        raw_items = payload.get("items") or []
        items = [NormalizedItem.from_mapping(item) for item in raw_items if isinstance(item, Mapping)] if isinstance(raw_items, list) else []
        return cls(
            provider=_coerce_str(payload.get("provider")),
            model=_coerce_str(payload.get("model")),
            currency=_coerce_str(payload.get("currency") or payload.get("currency_code")),
            merchant=_coerce_str(payload.get("merchant") or payload.get("vendor") or payload.get("payee")),
            date=_coerce_str(payload.get("date") or payload.get("transaction_date") or payload.get("receipt_date")),
            subtotal=_coerce_float(payload.get("subtotal")),
            tax=_coerce_float(payload.get("tax") or payload.get("tax_amount")),
            tip=_coerce_float(payload.get("tip") or payload.get("gratuity")),
            total=_coerce_float(payload.get("total") or payload.get("amount") or payload.get("grand_total")),
            notes=_coerce_str(payload.get("notes") or payload.get("memo") or payload.get("description")),
            items=items,
        )

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "provider": self.provider,
            "model": self.model,
            "currency": self.currency,
            "merchant": self.merchant,
            "date": self.date,
            "subtotal": self.subtotal,
            "tax": self.tax,
            "tip": self.tip,
            "total": self.total,
            "notes": self.notes,
            "items": [item.to_dict() for item in self.items],
        }
        return {k: v for k, v in data.items() if v not in (None, [], {})}


def load_request(payload: str | Mapping[str, Any]) -> DocumentRequest:
    if isinstance(payload, str):
        payload = json.loads(payload)
    return DocumentRequest.from_mapping(payload)


def load_response(payload: str | Mapping[str, Any]) -> DocumentResponse:
    if isinstance(payload, str):
        payload = json.loads(payload)
    return DocumentResponse.from_mapping(payload)


def normalize_expense_payload(payload: str | Mapping[str, Any]) -> NormalizedExpense:
    if isinstance(payload, str):
        payload = json.loads(payload)
    return NormalizedExpense.from_mapping(payload)


def normalize_field_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return FieldValue.from_any(value).to_dict()
    return value
