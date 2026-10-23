from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence


def _to_decimal(value: Any) -> Optional[Decimal]:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float, str)):
        try:
            return Decimal(str(value))
        except Exception:
            return None
    return None


def _to_float(value: Any) -> Optional[float]:
    d = _to_decimal(value)
    return float(d) if d is not None else None


def _to_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        s = value.strip()
        return s if s else None
    return str(value)


def _parse_date(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, date):
        return value.isoformat()
    s = _to_str(value)
    if not s:
        return None
    for parser in (
        lambda v: datetime.fromisoformat(v).date(),
        lambda v: datetime.strptime(v, "%Y-%m-%d").date(),
        lambda v: datetime.strptime(v, "%m/%d/%Y").date(),
        lambda v: datetime.strptime(v, "%d/%m/%Y").date(),
    ):
        try:
            return parser(s).isoformat()
        except Exception:
            pass
    return s


def _normalize_confidence(value: Any) -> Optional[float]:
    score = _to_float(value)
    if score is None:
        return None
    if score > 1.0:
        score = score / 100.0
    if score < 0.0:
        return 0.0
    if score > 1.0:
        return 1.0
    return score


@dataclass
class DocumentExtractionRequest:
    document_id: Optional[str] = None
    text: Optional[str] = None
    mime_type: Optional[str] = None
    filename: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_id": self.document_id,
            "text": self.text,
            "mime_type": self.mime_type,
            "filename": self.filename,
            "metadata": dict(self.metadata),
        }


@dataclass
class DocumentField:
    name: str
    value: Any = None
    confidence: Optional[float] = None
    source: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "confidence": self.confidence,
            "source": self.source,
        }


@dataclass
class DocumentExtractionResponse:
    fields: List[DocumentField] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)
    normalized: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fields": [f.to_dict() for f in self.fields],
            "raw": dict(self.raw),
            "normalized": dict(self.normalized),
            "warnings": list(self.warnings),
        }


def normalize_document_fields(payload: Mapping[str, Any]) -> Dict[str, Any]:
    data = dict(payload or {})
    normalized: Dict[str, Any] = {}

    vendor = data.get("vendor") or data.get("merchant")
    if vendor is not None:
        normalized["vendor"] = _to_str(vendor)

    doc_date = data.get("date") or data.get("invoice_date") or data.get("receipt_date")
    if doc_date is not None:
        normalized["date"] = _parse_date(doc_date)

    total = data.get("total") or data.get("amount") or data.get("grand_total")
    if total is not None:
        normalized["total"] = _to_decimal(total)

    tax = data.get("tax") or data.get("tax_amount")
    if tax is not None:
        normalized["tax"] = _to_decimal(tax)

    currency = data.get("currency")
    if currency is not None:
        normalized["currency"] = _to_str(currency)

    notes = data.get("notes") or data.get("memo") or data.get("description")
    if notes is not None:
        normalized["notes"] = _to_str(notes)

    items = data.get("items") or data.get("line_items") or []
    normalized_items: List[Dict[str, Any]] = []
    if isinstance(items, Sequence) and not isinstance(items, (str, bytes)):
        for item in items:
            if isinstance(item, Mapping):
                normalized_items.append(
                    {
                        "description": _to_str(item.get("description") or item.get("name")),
                        "quantity": _to_float(item.get("quantity")),
                        "unit_price": _to_decimal(item.get("unit_price") or item.get("price")),
                        "amount": _to_decimal(item.get("amount") or item.get("total")),
                    }
                )
    if normalized_items:
        normalized["items"] = normalized_items

    confidence = data.get("confidence")
    if confidence is not None:
        normalized["confidence"] = _normalize_confidence(confidence)

    for key, value in data.items():
        if key not in normalized:
            normalized[key] = value

    return normalized


def build_extraction_response(raw: Mapping[str, Any]) -> DocumentExtractionResponse:
    normalized = normalize_document_fields(raw)
    fields: List[DocumentField] = []
    for key, value in normalized.items():
        if key == "items" and isinstance(value, list):
            continue
        fields.append(DocumentField(name=key, value=value, confidence=_normalize_confidence(raw.get(f"{key}_confidence"))))
    return DocumentExtractionResponse(fields=fields, raw=dict(raw), normalized=normalized)
