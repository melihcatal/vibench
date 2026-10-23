from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


JSONScalar = Union[str, int, float, bool, None]
JSONValue = Union[JSONScalar, Dict[str, Any], List[Any]]


def _coerce_decimal(value: Any) -> Optional[Decimal]:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, bool):
        return Decimal(int(value))
    if isinstance(value, (int, float, str)):
        text = str(value).strip()
        if text == "":
            return None
        try:
            return Decimal(text)
        except Exception:
            return None
    return None


def _coerce_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _coerce_date(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, date):
        return value.isoformat()
    text = _coerce_str(value)
    if not text:
        return None
    for parser in (
        lambda t: datetime.fromisoformat(t).date().isoformat(),
        lambda t: date.fromisoformat(t).isoformat(),
    ):
        try:
            return parser(text)
        except Exception:
            pass
    return text


def _coerce_float(value: Any) -> Optional[float]:
    dec = _coerce_decimal(value)
    return float(dec) if dec is not None else None


@dataclass
class DocumentField:
    name: str
    value: Any = None
    confidence: Optional[float] = None
    normalized_value: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "DocumentField":
        return cls(
            name=_coerce_str(data.get("name")) or "",
            value=data.get("value"),
            confidence=_coerce_float(data.get("confidence")),
            normalized_value=data.get("normalized_value"),
            metadata=dict(data.get("metadata") or {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LineItem:
    description: Optional[str] = None
    quantity: Optional[Decimal] = None
    unit_price: Optional[Decimal] = None
    total: Optional[Decimal] = None
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "LineItem":
        return cls(
            description=_coerce_str(data.get("description")),
            quantity=_coerce_decimal(data.get("quantity")),
            unit_price=_coerce_decimal(data.get("unit_price")),
            total=_coerce_decimal(data.get("total")),
            confidence=_coerce_float(data.get("confidence")),
            metadata=dict(data.get("metadata") or {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        for key in ("quantity", "unit_price", "total"):
            if payload[key] is not None:
                payload[key] = str(payload[key])
        return payload


@dataclass
class StructuredDocumentRequest:
    document_id: Optional[str] = None
    document_url: Optional[str] = None
    document_text: Optional[str] = None
    mime_type: Optional[str] = None
    locale: Optional[str] = None
    schema_name: Optional[str] = None
    options: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "StructuredDocumentRequest":
        return cls(
            document_id=_coerce_str(data.get("document_id")),
            document_url=_coerce_str(data.get("document_url")),
            document_text=_coerce_str(data.get("document_text")),
            mime_type=_coerce_str(data.get("mime_type")),
            locale=_coerce_str(data.get("locale")),
            schema_name=_coerce_str(data.get("schema_name")),
            options=dict(data.get("options") or {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class StructuredDocumentResponse:
    document_id: Optional[str] = None
    schema_name: Optional[str] = None
    fields: List[DocumentField] = field(default_factory=list)
    line_items: List[LineItem] = field(default_factory=list)
    normalized: Dict[str, Any] = field(default_factory=dict)
    confidence: Optional[float] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "StructuredDocumentResponse":
        fields = [DocumentField.from_mapping(item) for item in data.get("fields") or []]
        line_items = [LineItem.from_mapping(item) for item in data.get("line_items") or []]
        return cls(
            document_id=_coerce_str(data.get("document_id")),
            schema_name=_coerce_str(data.get("schema_name")),
            fields=fields,
            line_items=line_items,
            normalized=dict(data.get("normalized") or {}),
            confidence=_coerce_float(data.get("confidence")),
            raw=dict(data.get("raw") or {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_id": self.document_id,
            "schema_name": self.schema_name,
            "fields": [field.to_dict() for field in self.fields],
            "line_items": [item.to_dict() for item in self.line_items],
            "normalized": self.normalized,
            "confidence": self.confidence,
            "raw": self.raw,
        }


@dataclass
class NormalizedExpenseRecord:
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[Decimal] = None
    currency: Optional[str] = None
    tax_amount: Optional[Decimal] = None
    tips_amount: Optional[Decimal] = None
    notes: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "NormalizedExpenseRecord":
        return cls(
            vendor_name=_coerce_str(data.get("vendor_name")),
            transaction_date=_coerce_date(data.get("transaction_date")),
            total_amount=_coerce_decimal(data.get("total_amount")),
            currency=_coerce_str(data.get("currency")),
            tax_amount=_coerce_decimal(data.get("tax_amount")),
            tips_amount=_coerce_decimal(data.get("tips_amount")),
            notes=_coerce_str(data.get("notes")),
            line_items=[LineItem.from_mapping(item) for item in data.get("line_items") or []],
            metadata=dict(data.get("metadata") or {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        if payload["total_amount"] is not None:
            payload["total_amount"] = str(payload["total_amount"])
        if payload["tax_amount"] is not None:
            payload["tax_amount"] = str(payload["tax_amount"])
        if payload["tips_amount"] is not None:
            payload["tips_amount"] = str(payload["tips_amount"])
        payload["line_items"] = [item.to_dict() for item in self.line_items]
        return payload


def normalize_document_fields(data: Mapping[str, Any]) -> Dict[str, Any]:
    return StructuredDocumentResponse.from_mapping(data).to_dict()


def normalize_expense_record(data: Mapping[str, Any]) -> Dict[str, Any]:
    return NormalizedExpenseRecord.from_mapping(data).to_dict()
