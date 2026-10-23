from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping, MutableMapping, Sequence


def _to_decimal(value: Any) -> Decimal | None:
    if value is None or value == "":
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    if isinstance(value, str):
        try:
            return Decimal(value.strip())
        except (InvalidOperation, AttributeError):
            return None
    return None


def _to_date(value: Any) -> str | None:
    if value is None or value == "":
        return None
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, str):
        text = value.strip()
        for parser in (date.fromisoformat,):
            try:
                return parser(text).isoformat()
            except ValueError:
                pass
    return None


def _to_float(value: Any) -> float | None:
    dec = _to_decimal(value)
    return float(dec) if dec is not None else None


def _normalize_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


@dataclass(slots=True)
class DocumentExtractionRequest:
    document_id: str | None = None
    file_name: str | None = None
    mime_type: str | None = None
    locale: str | None = None
    fields: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "DocumentExtractionRequest":
        return cls(
            document_id=_normalize_text(payload.get("document_id")),
            file_name=_normalize_text(payload.get("file_name")),
            mime_type=_normalize_text(payload.get("mime_type")),
            locale=_normalize_text(payload.get("locale")),
            fields=[str(item) for item in payload.get("fields", []) or []],
            metadata=dict(payload.get("metadata", {}) or {}),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class LineItem:
    description: str | None = None
    quantity: float | None = None
    unit_price: float | None = None
    amount: float | None = None
    confidence: float | None = None

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "LineItem":
        return cls(
            description=_normalize_text(payload.get("description")),
            quantity=_to_float(payload.get("quantity")),
            unit_price=_to_float(payload.get("unit_price")),
            amount=_to_float(payload.get("amount")),
            confidence=_to_float(payload.get("confidence")),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DocumentExtractionResponse:
    document_id: str | None = None
    status: str | None = None
    vendor: str | None = None
    merchant: str | None = None
    invoice_date: str | None = None
    total: float | None = None
    tax: float | None = None
    notes: str | None = None
    summary: str | None = None
    confidence: float | None = None
    items: list[LineItem] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "DocumentExtractionResponse":
        items_payload = payload.get("items", []) or []
        items = [LineItem.from_mapping(item) for item in items_payload if isinstance(item, Mapping)]
        return cls(
            document_id=_normalize_text(payload.get("document_id")),
            status=_normalize_text(payload.get("status")),
            vendor=_normalize_text(payload.get("vendor")),
            merchant=_normalize_text(payload.get("merchant")),
            invoice_date=_to_date(payload.get("invoice_date") or payload.get("date")),
            total=_to_float(payload.get("total")),
            tax=_to_float(payload.get("tax")),
            notes=_normalize_text(payload.get("notes") or payload.get("memo")),
            summary=_normalize_text(payload.get("summary")),
            confidence=_to_float(payload.get("confidence")),
            items=items,
            raw=dict(payload),
        )

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["items"] = [item.to_dict() for item in self.items]
        return data


def normalize_extracted_document(payload: Mapping[str, Any]) -> dict[str, Any]:
    response = DocumentExtractionResponse.from_mapping(payload)
    normalized_items: list[dict[str, Any]] = []
    for item in response.items:
        normalized_items.append(
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "amount": item.amount,
                "confidence": item.confidence,
            }
        )
    return {
        "document_id": response.document_id,
        "vendor": response.vendor or response.merchant,
        "merchant": response.merchant or response.vendor,
        "invoice_date": response.invoice_date,
        "total": response.total,
        "tax": response.tax,
        "notes": response.notes,
        "summary": response.summary,
        "confidence": response.confidence,
        "items": normalized_items,
        "raw": response.raw,
    }


def merge_normalized_fields(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    merged: MutableMapping[str, Any] = dict(base)
    for key, value in override.items():
        if value is not None and value != "":
            merged[key] = value
    return dict(merged)


def coerce_field_names(fields: Sequence[Any]) -> list[str]:
    return [str(field).strip() for field in fields if _normalize_text(field) is not None]
