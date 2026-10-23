import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


def _as_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip())
    except Exception:
        return None


def _as_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


@dataclass
class DocumentExtractionRequest:
    document_id: Optional[str] = None
    document_url: Optional[str] = None
    document_base64: Optional[str] = None
    mime_type: Optional[str] = None
    schema: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            key: value
            for key, value in asdict(self).items()
            if value not in (None, {}, [], "")
        }


@dataclass
class DocumentExtractionResponse:
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    raw: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    request_id: Optional[str] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "DocumentExtractionResponse":
        return cls(
            success=bool(payload.get("success", payload.get("ok", True))),
            data=dict(payload.get("data") or payload.get("result") or payload.get("fields") or {}),
            raw=payload,
            error=payload.get("error"),
            request_id=payload.get("request_id") or payload.get("id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "success": self.success,
            "data": self.data,
            "raw": self.raw,
            "error": self.error,
            "request_id": self.request_id,
        }
        return {k: v for k, v in payload.items() if v not in (None, {}, [], "")}


def normalize_field_mapping(fields: Dict[str, Any], mapping: Dict[str, List[str]]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    for target, aliases in mapping.items():
        value = None
        for key in [target, *aliases]:
            if key in fields and fields[key] not in (None, "", [], {}):
                value = fields[key]
                break
        normalized[target] = value
    return normalized


def normalize_money_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(fields)
    for key in ("subtotal", "tax", "tip", "total", "amount", "unit_price"):
        if key in normalized:
            normalized[key] = _as_float(normalized.get(key))
    if "currency" in normalized:
        normalized["currency"] = _as_str(normalized.get("currency"))
    return normalized


def normalize_line_items(items: Any) -> List[Dict[str, Any]]:
    if not isinstance(items, list):
        return []
    normalized_items: List[Dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        normalized_items.append(
            {
                "description": _as_str(item.get("description") or item.get("name") or item.get("text")),
                "quantity": _as_float(item.get("quantity")),
                "unit_price": _as_float(item.get("unit_price") or item.get("price")),
                "amount": _as_float(item.get("amount") or item.get("total")),
            }
        )
    return normalized_items


def build_standard_expense_schema(fields: Dict[str, Any]) -> Dict[str, Any]:
    normalized = normalize_field_mapping(
        fields,
        {
            "merchant": ["vendor", "merchant_name", "seller"],
            "date": ["transaction_date", "invoice_date", "receipt_date"],
            "currency": [],
            "subtotal": [],
            "tax": [],
            "tip": [],
            "total": [],
            "payment_method": ["payment", "tender"],
            "category": [],
            "notes": ["memo", "description", "remarks"],
            "confidence": [],
        },
    )
    normalized = normalize_money_fields(normalized)
    normalized["items"] = normalize_line_items(fields.get("items") or fields.get("line_items") or [])
    return normalized


def dumps_normalized(fields: Dict[str, Any]) -> str:
    return json.dumps(build_standard_expense_schema(fields), ensure_ascii=False, sort_keys=True)
