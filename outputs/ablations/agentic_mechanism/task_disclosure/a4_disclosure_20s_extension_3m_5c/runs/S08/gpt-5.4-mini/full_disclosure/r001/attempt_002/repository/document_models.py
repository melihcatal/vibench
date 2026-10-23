from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Union


JsonScalar = Union[str, int, float, bool, None]
JsonValue = Union[JsonScalar, List["JsonValue"], Dict[str, "JsonValue"]]


def _to_decimal(value: Any) -> Optional[Decimal]:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float, str)):
        text = str(value).strip()
        if not text:
            return None
        try:
            return Decimal(text)
        except Exception:
            return None
    return None


def _to_float(value: Any) -> Optional[float]:
    decimal_value = _to_decimal(value)
    if decimal_value is None:
        return None
    return float(decimal_value)


def _normalize_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _normalize_list(values: Any) -> List[Any]:
    if values is None:
        return []
    if isinstance(values, (list, tuple)):
        return list(values)
    return [values]


@dataclass
class FieldConfidence:
    value: Any = None
    confidence: Optional[float] = None
    normalized: Any = None

    @classmethod
    def from_any(cls, value: Any) -> "FieldConfidence":
        if isinstance(value, cls):
            return value
        if isinstance(value, Mapping):
            return cls(
                value=value.get("value"),
                confidence=_to_float(value.get("confidence")),
                normalized=value.get("normalized"),
            )
        return cls(value=value)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"value": self.value}
        if self.confidence is not None:
            data["confidence"] = self.confidence
        if self.normalized is not None:
            data["normalized"] = self.normalized
        return data


@dataclass
class LineItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_any(cls, value: Any) -> "LineItem":
        if isinstance(value, cls):
            return value
        if isinstance(value, Mapping):
            known = {k: v for k, v in value.items() if k not in {"description", "quantity", "unit_price", "amount", "confidence"}}
            return cls(
                description=_normalize_str(value.get("description")),
                quantity=_to_float(value.get("quantity")),
                unit_price=_to_float(value.get("unit_price")),
                amount=_to_float(value.get("amount")),
                confidence=_to_float(value.get("confidence")),
                extra=dict(known),
            )
        return cls(description=_normalize_str(value))

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = dict(self.extra)
        if self.description is not None:
            data["description"] = self.description
        if self.quantity is not None:
            data["quantity"] = self.quantity
        if self.unit_price is not None:
            data["unit_price"] = self.unit_price
        if self.amount is not None:
            data["amount"] = self.amount
        if self.confidence is not None:
            data["confidence"] = self.confidence
        return data


@dataclass
class DocumentExtractionRequest:
    document_id: Optional[str] = None
    document_type: Optional[str] = None
    locale: Optional[str] = None
    source_uri: Optional[str] = None
    text: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "DocumentExtractionRequest":
        return cls(
            document_id=_normalize_str(payload.get("document_id")),
            document_type=_normalize_str(payload.get("document_type")),
            locale=_normalize_str(payload.get("locale")),
            source_uri=_normalize_str(payload.get("source_uri")),
            text=_normalize_str(payload.get("text")),
            metadata=dict(payload.get("metadata") or {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = dict(self.metadata)
        if self.document_id is not None:
            data["document_id"] = self.document_id
        if self.document_type is not None:
            data["document_type"] = self.document_type
        if self.locale is not None:
            data["locale"] = self.locale
        if self.source_uri is not None:
            data["source_uri"] = self.source_uri
        if self.text is not None:
            data["text"] = self.text
        return data


@dataclass
class DocumentExtractionResponse:
    document_id: Optional[str] = None
    document_type: Optional[str] = None
    fields: Dict[str, FieldConfidence] = field(default_factory=dict)
    line_items: List[LineItem] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "DocumentExtractionResponse":
        fields_payload = payload.get("fields") or {}
        fields: Dict[str, FieldConfidence] = {}
        for key, value in fields_payload.items():
            fields[str(key)] = FieldConfidence.from_any(value)
        line_items = [LineItem.from_any(item) for item in _normalize_list(payload.get("line_items"))]
        return cls(
            document_id=_normalize_str(payload.get("document_id")),
            document_type=_normalize_str(payload.get("document_type")),
            fields=fields,
            line_items=line_items,
            raw=dict(payload),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_id": self.document_id,
            "document_type": self.document_type,
            "fields": {key: value.to_dict() for key, value in self.fields.items()},
            "line_items": [item.to_dict() for item in self.line_items],
            "raw": dict(self.raw),
        }


@dataclass
class NormalizedExpenseRecord:
    vendor: Optional[str] = None
    transaction_date: Optional[str] = None
    currency: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    notes: Optional[str] = None
    merchant: Optional[str] = None
    items: List[LineItem] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "NormalizedExpenseRecord":
        items = [LineItem.from_any(item) for item in _normalize_list(payload.get("items"))]
        return cls(
            vendor=_normalize_str(payload.get("vendor")),
            transaction_date=_normalize_str(payload.get("transaction_date")),
            currency=_normalize_str(payload.get("currency")),
            total=_to_float(payload.get("total")),
            tax=_to_float(payload.get("tax")),
            notes=_normalize_str(payload.get("notes")),
            merchant=_normalize_str(payload.get("merchant")),
            items=items,
            metadata=dict(payload.get("metadata") or {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = dict(self.metadata)
        if self.vendor is not None:
            data["vendor"] = self.vendor
        if self.transaction_date is not None:
            data["transaction_date"] = self.transaction_date
        if self.currency is not None:
            data["currency"] = self.currency
        if self.total is not None:
            data["total"] = self.total
        if self.tax is not None:
            data["tax"] = self.tax
        if self.notes is not None:
            data["notes"] = self.notes
        if self.merchant is not None:
            data["merchant"] = self.merchant
        if self.items:
            data["items"] = [item.to_dict() for item in self.items]
        return data


def normalize_document_payload(payload: Mapping[str, Any]) -> Dict[str, Any]:
    request = DocumentExtractionRequest.from_dict(payload)
    return request.to_dict()


def normalize_extraction_response(payload: Mapping[str, Any]) -> Dict[str, Any]:
    response = DocumentExtractionResponse.from_dict(payload)
    return response.to_dict()


def normalize_expense_payload(payload: Mapping[str, Any]) -> Dict[str, Any]:
    record = NormalizedExpenseRecord.from_dict(payload)
    return record.to_dict()
