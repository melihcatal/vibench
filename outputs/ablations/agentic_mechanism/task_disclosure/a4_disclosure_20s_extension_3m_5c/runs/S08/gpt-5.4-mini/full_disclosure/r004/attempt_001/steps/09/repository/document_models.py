from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, Sequence


def _to_decimal(value: Any) -> Optional[Decimal]:
    if value is None or value == "":
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, bool):
        return Decimal(int(value))
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    if isinstance(value, str):
        return Decimal(value.strip())
    return None


def _to_float(value: Any) -> Optional[float]:
    dec = _to_decimal(value)
    return float(dec) if dec is not None else None


def _to_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _to_date(value: Any) -> Optional[str]:
    if value is None or value == "":
        return None
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, datetime):
        return value.date().isoformat()
    text = str(value).strip()
    for parser in (
        lambda s: datetime.fromisoformat(s).date(),
        lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        lambda s: datetime.strptime(s, "%m/%d/%Y").date(),
        lambda s: datetime.strptime(s, "%d/%m/%Y").date(),
    ):
        try:
            return parser(text).isoformat()
        except Exception:
            continue
    return text


@dataclass
class FieldEvidence:
    value: Any
    confidence: Optional[float] = None
    source: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "confidence": self.confidence,
            "source": self.source,
        }


@dataclass
class ExtractionRequest:
    document_id: Optional[str] = None
    document_type: Optional[str] = None
    text: Optional[str] = None
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_id": self.document_id,
            "document_type": self.document_type,
            "text": self.text,
            "language": self.language,
            "metadata": dict(self.metadata),
        }


@dataclass
class ExtractionResponse:
    document_id: Optional[str] = None
    fields: Dict[str, Any] = field(default_factory=dict)
    confidences: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)
    normalized: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_id": self.document_id,
            "fields": dict(self.fields),
            "confidences": dict(self.confidences),
            "raw": dict(self.raw),
            "normalized": dict(self.normalized),
        }


@dataclass
class LineItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "amount": self.amount,
            "confidence": self.confidence,
        }


@dataclass
class InvoiceFields:
    vendor: Optional[str] = None
    invoice_date: Optional[str] = None
    total: Optional[float] = None
    currency: Optional[str] = None
    notes: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vendor": self.vendor,
            "invoice_date": self.invoice_date,
            "total": self.total,
            "currency": self.currency,
            "notes": self.notes,
            "line_items": [item.to_dict() for item in self.line_items],
            "confidence": self.confidence,
        }


@dataclass
class ReceiptFields:
    merchant: Optional[str] = None
    purchase_date: Optional[str] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    currency: Optional[str] = None
    items: List[LineItem] = field(default_factory=list)
    confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "merchant": self.merchant,
            "purchase_date": self.purchase_date,
            "tax": self.tax,
            "total": self.total,
            "currency": self.currency,
            "items": [item.to_dict() for item in self.items],
            "confidence": self.confidence,
        }


@dataclass
class NormalizedExpenseRecord:
    document_id: Optional[str] = None
    document_type: Optional[str] = None
    merchant: Optional[str] = None
    vendor: Optional[str] = None
    transaction_date: Optional[str] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    currency: Optional[str] = None
    notes: Optional[str] = None
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    source: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_id": self.document_id,
            "document_type": self.document_type,
            "merchant": self.merchant,
            "vendor": self.vendor,
            "transaction_date": self.transaction_date,
            "subtotal": self.subtotal,
            "tax": self.tax,
            "total": self.total,
            "currency": self.currency,
            "notes": self.notes,
            "line_items": list(self.line_items),
            "source": dict(self.source),
        }


def normalize_invoice_fields(fields: Any) -> Dict[str, Any]:
    if isinstance(fields, InvoiceFields):
        payload = fields.to_dict()
    else:
        payload = dict(fields or {})
    payload["vendor"] = _to_str(payload.get("vendor"))
    payload["invoice_date"] = _to_date(payload.get("invoice_date"))
    payload["total"] = _to_float(payload.get("total"))
    payload["currency"] = _to_str(payload.get("currency"))
    payload["notes"] = _to_str(payload.get("notes"))
    items = payload.get("line_items") or []
    payload["line_items"] = [normalize_line_item(item) for item in items]
    payload["confidence"] = _to_float(payload.get("confidence"))
    return payload


def normalize_receipt_fields(fields: Any) -> Dict[str, Any]:
    if isinstance(fields, ReceiptFields):
        payload = fields.to_dict()
    else:
        payload = dict(fields or {})
    payload["merchant"] = _to_str(payload.get("merchant"))
    payload["purchase_date"] = _to_date(payload.get("purchase_date"))
    payload["tax"] = _to_float(payload.get("tax"))
    payload["total"] = _to_float(payload.get("total"))
    payload["currency"] = _to_str(payload.get("currency"))
    items = payload.get("items") or []
    payload["items"] = [normalize_line_item(item) for item in items]
    payload["confidence"] = _to_float(payload.get("confidence"))
    return payload


def normalize_line_item(item: Any) -> Dict[str, Any]:
    if isinstance(item, LineItem):
        payload = item.to_dict()
    else:
        payload = dict(item or {})
    return {
        "description": _to_str(payload.get("description")),
        "quantity": _to_float(payload.get("quantity")),
        "unit_price": _to_float(payload.get("unit_price")),
        "amount": _to_float(payload.get("amount")),
        "confidence": _to_float(payload.get("confidence")),
    }


def normalize_expense_record(record: Any) -> Dict[str, Any]:
    if isinstance(record, NormalizedExpenseRecord):
        payload = record.to_dict()
    else:
        payload = dict(record or {})
    payload["document_id"] = _to_str(payload.get("document_id"))
    payload["document_type"] = _to_str(payload.get("document_type"))
    payload["merchant"] = _to_str(payload.get("merchant"))
    payload["vendor"] = _to_str(payload.get("vendor"))
    payload["transaction_date"] = _to_date(payload.get("transaction_date"))
    payload["subtotal"] = _to_float(payload.get("subtotal"))
    payload["tax"] = _to_float(payload.get("tax"))
    payload["total"] = _to_float(payload.get("total"))
    payload["currency"] = _to_str(payload.get("currency"))
    payload["notes"] = _to_str(payload.get("notes"))
    payload["line_items"] = [normalize_line_item(item) for item in (payload.get("line_items") or [])]
    payload["source"] = dict(payload.get("source") or {})
    return payload


def response_from_fields(document_id: Optional[str], fields: Any, raw: Optional[Dict[str, Any]] = None) -> ExtractionResponse:
    normalized = fields
    if isinstance(fields, InvoiceFields):
        normalized = normalize_invoice_fields(fields)
    elif isinstance(fields, ReceiptFields):
        normalized = normalize_receipt_fields(fields)
    elif isinstance(fields, NormalizedExpenseRecord):
        normalized = normalize_expense_record(fields)
    elif isinstance(fields, dict):
        normalized = dict(fields)
    else:
        normalized = asdict(fields) if hasattr(fields, "__dataclass_fields__") else {}
    return ExtractionResponse(document_id=document_id, fields=normalized, raw=dict(raw or {}), normalized=dict(normalized))
