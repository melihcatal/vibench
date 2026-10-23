from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


@dataclass
class StructuredDocumentRequest:
    document_type: str
    text: str
    document_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def schema_hint(self) -> dict[str, Any]:
        if self.document_type == "invoice":
            return {"vendor": "string", "date": "string", "total": "number", "line_items": [{"description": "string", "quantity": "number", "unit_price": "number", "amount": "number"}]}
        if self.document_type == "receipt":
            return {"merchant": "string", "tax": "number", "total": "number", "items": [{"description": "string", "quantity": "number", "amount": "number"}]}
        return {"fields": "object"}


def _is_number(value: Any) -> bool:
    try:
        return value is not None and not isinstance(value, bool) and math.isfinite(float(value))
    except Exception:
        return False


def coerce_invoice_extraction(payload: dict) -> dict:
    return {"vendor": payload.get("vendor"), "date": payload.get("date"), "total": float(payload["total"]) if _is_number(payload.get("total")) else payload.get("total"), "line_items": payload.get("line_items", [])}


def coerce_receipt_extraction(payload: dict) -> dict:
    return {"merchant": payload.get("merchant"), "tax": float(payload["tax"]) if _is_number(payload.get("tax")) else payload.get("tax"), "total": float(payload["total"]) if _is_number(payload.get("total")) else payload.get("total"), "items": payload.get("items", [])}


def normalize_expense_record(extracted: dict) -> dict:
    return {"source_type": extracted.get("document_type") or extracted.get("type") or "expense", "vendor": extracted.get("vendor") or extracted.get("merchant"), "date": extracted.get("date"), "currency": extracted.get("currency", "USD"), "subtotal": extracted.get("subtotal"), "tax": extracted.get("tax"), "total": extracted.get("total"), "line_items": extracted.get("line_items") or extracted.get("items") or []}


def validate_structured_document(payload: dict) -> dict:
    required = ["total"]
    missing = [k for k in required if payload.get(k) in (None, "")]
    confidence = payload.get("confidence_scores", {}) if isinstance(payload.get("confidence_scores"), dict) else {}
    low_confidence = [k for k, v in confidence.items() if _is_number(v) and float(v) < 0.8]
    return {"valid": not missing and not low_confidence, "missing_fields": missing, "low_confidence_fields": low_confidence, "confidence_scores": confidence}
