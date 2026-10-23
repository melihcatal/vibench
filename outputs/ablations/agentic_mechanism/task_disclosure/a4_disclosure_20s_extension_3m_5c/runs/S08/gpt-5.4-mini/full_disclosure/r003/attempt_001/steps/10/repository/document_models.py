from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union


JsonValue = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]


def _to_decimal(value: Any) -> Optional[Decimal]:
    if value is None or value == "":
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    if isinstance(value, str):
        try:
            return Decimal(value.strip())
        except Exception:
            return None
    return None


def _to_float(value: Any) -> Optional[float]:
    dec = _to_decimal(value)
    return float(dec) if dec is not None else None


def _parse_date(value: Any) -> Optional[str]:
    if value is None or value == "":
        return None
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, str):
        text = value.strip()
        for parser in (
            lambda s: date.fromisoformat(s),
            lambda s: datetime.fromisoformat(s).date(),
        ):
            try:
                return parser(text).isoformat()
            except Exception:
                continue
    return None


def _confidence(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        confidence = float(value)
    except Exception:
        return None
    if confidence < 0:
        return 0.0
    if confidence > 1:
        return 1.0
    return confidence


@dataclass
class FieldValue:
    value: Any
    confidence: Optional[float] = None
    source: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"value": self.value}
        if self.confidence is not None:
            payload["confidence"] = self.confidence
        if self.source is not None:
            payload["source"] = self.source
        return payload

    @classmethod
    def from_value(cls, value: Any) -> "FieldValue":
        if isinstance(value, cls):
            return value
        if isinstance(value, Mapping):
            return cls(
                value=value.get("value"),
                confidence=_confidence(value.get("confidence")),
                source=value.get("source"),
            )
        return cls(value=value)


@dataclass
class LineItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
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

    @classmethod
    def from_value(cls, value: Any) -> "LineItem":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            return cls(description=str(value) if value is not None else None)
        return cls(
            description=value.get("description") or value.get("name"),
            quantity=_to_float(value.get("quantity")),
            unit_price=_to_float(value.get("unit_price") or value.get("unitPrice")),
            amount=_to_float(value.get("amount") or value.get("total")),
            confidence=_confidence(value.get("confidence")),
        )


@dataclass
class DocumentExtractionRequest:
    document_id: Optional[str] = None
    document_type: Optional[str] = None
    locale: Optional[str] = None
    fields: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {}
        if self.document_id is not None:
            payload["document_id"] = self.document_id
        if self.document_type is not None:
            payload["document_type"] = self.document_type
        if self.locale is not None:
            payload["locale"] = self.locale
        if self.fields:
            payload["fields"] = list(self.fields)
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass
class StructuredDocumentResponse:
    document_type: Optional[str] = None
    extracted_fields: Dict[str, FieldValue] = field(default_factory=dict)
    line_items: List[LineItem] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_type": self.document_type,
            "extracted_fields": {k: v.to_dict() for k, v in self.extracted_fields.items()},
            "line_items": [item.to_dict() for item in self.line_items],
            "raw": dict(self.raw),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "StructuredDocumentResponse":
        extracted = payload.get("extracted_fields") or payload.get("fields") or {}
        items = payload.get("line_items") or payload.get("items") or []
        fields: Dict[str, FieldValue] = {}
        if isinstance(extracted, Mapping):
            for key, value in extracted.items():
                fields[str(key)] = FieldValue.from_value(value)
        return cls(
            document_type=payload.get("document_type") or payload.get("type"),
            extracted_fields=fields,
            line_items=[LineItem.from_value(item) for item in items if item is not None],
            raw=dict(payload),
        )


@dataclass
class NormalizedExpenseRecord:
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    transaction_date: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    currency: Optional[str] = None
    notes: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        if self.vendor is not None:
            data["vendor"] = self.vendor
        if self.merchant is not None:
            data["merchant"] = self.merchant
        if self.transaction_date is not None:
            data["transaction_date"] = self.transaction_date
        if self.total is not None:
            data["total"] = self.total
        if self.tax is not None:
            data["tax"] = self.tax
        if self.currency is not None:
            data["currency"] = self.currency
        if self.notes is not None:
            data["notes"] = self.notes
        if self.line_items:
            data["line_items"] = [item.to_dict() for item in self.line_items]
        if self.confidence is not None:
            data["confidence"] = self.confidence
        return data

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "NormalizedExpenseRecord":
        return cls(
            vendor=payload.get("vendor"),
            merchant=payload.get("merchant"),
            transaction_date=_parse_date(payload.get("transaction_date") or payload.get("date")),
            total=_to_float(payload.get("total")),
            tax=_to_float(payload.get("tax")),
            currency=payload.get("currency"),
            notes=payload.get("notes"),
            line_items=[LineItem.from_value(item) for item in (payload.get("line_items") or []) if item is not None],
            confidence=_confidence(payload.get("confidence")),
        )


def normalize_extracted_fields(payload: Mapping[str, Any]) -> NormalizedExpenseRecord:
    if isinstance(payload, StructuredDocumentResponse):
        payload = payload.to_dict()
    if "extracted_fields" in payload:
        fields = payload.get("extracted_fields") or {}
    else:
        fields = payload
    vendor = None
    merchant = None
    transaction_date = None
    total = None
    tax = None
    currency = None
    notes = None
    confidence_values: List[float] = []
    if isinstance(fields, Mapping):
        for key, raw in fields.items():
            fv = FieldValue.from_value(raw)
            key_l = str(key).lower()
            if key_l in {"vendor", "supplier", "payee"}:
                vendor = fv.value if fv.value is not None else vendor
            elif key_l in {"merchant", "store", "business"}:
                merchant = fv.value if fv.value is not None else merchant
            elif key_l in {"date", "transaction_date", "invoice_date", "receipt_date"}:
                transaction_date = _parse_date(fv.value) or transaction_date
            elif key_l in {"total", "amount", "grand_total"}:
                total = _to_float(fv.value) if fv.value is not None else total
            elif key_l in {"tax", "vat", "sales_tax"}:
                tax = _to_float(fv.value) if fv.value is not None else tax
            elif key_l == "currency":
                currency = str(fv.value) if fv.value is not None else currency
            elif key_l in {"notes", "memo", "description", "vendor_notes"}:
                notes = str(fv.value) if fv.value is not None else notes
            if fv.confidence is not None:
                confidence_values.append(fv.confidence)
    line_items = []
    for item in payload.get("line_items", []) if isinstance(payload, Mapping) else []:
        line_items.append(LineItem.from_value(item))
    confidence = sum(confidence_values) / len(confidence_values) if confidence_values else None
    return NormalizedExpenseRecord(
        vendor=str(vendor) if vendor is not None else None,
        merchant=str(merchant) if merchant is not None else None,
        transaction_date=transaction_date,
        total=total,
        tax=tax,
        currency=currency,
        notes=notes,
        line_items=line_items,
        confidence=confidence,
    )
