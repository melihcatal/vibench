from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class StructuredDocumentExtractionRequest:
    document_text: str
    schema: Dict[str, Any]
    instructions: str = "Extract the document into the provided JSON schema."

    def to_payload(self) -> Dict[str, Any]:
        return {
            "document_text": self.document_text,
            "schema": self.schema,
            "instructions": self.instructions,
        }


@dataclass(frozen=True)
class StructuredDocumentExtractionResponse:
    data: Dict[str, Any]
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        return {"data": self.data, "raw_response": self.raw_response}


def parse_amount(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, (int, float, Decimal)):
        return str(Decimal(str(value)).quantize(Decimal("0.01")))
    text = str(value).strip()
    if not text:
        return None
    cleaned = "".join(ch for ch in text if ch.isdigit() or ch in {"-", ",", "."})
    if not cleaned:
        return None
    if cleaned.count(",") > 0 and cleaned.count(".") == 0:
        cleaned = cleaned.replace(",", ".")
    elif cleaned.count(",") > 0 and cleaned.count(".") > 0:
        cleaned = cleaned.replace(",", "")
    try:
        return str(Decimal(cleaned).quantize(Decimal("0.01")))
    except (InvalidOperation, ValueError):
        return None


def parse_date(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    text = str(value).strip()
    if not text:
        return None
    formats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%b %d, %Y", "%B %d, %Y"]
    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return None


def normalize_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def normalize_structured_document_fields(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {
        "schema_version": "1.0",
        "normalized_at": datetime.now(timezone.utc).isoformat(),
        "document": {
            "document_type": normalize_text(extracted_fields.get("document_type")),
            "document_id": normalize_text(extracted_fields.get("document_id") or extracted_fields.get("id")),
            "date": parse_date(extracted_fields.get("date")),
            "total": parse_amount(extracted_fields.get("total") or extracted_fields.get("amount")),
            "currency": normalize_text(extracted_fields.get("currency") or extracted_fields.get("ccy")),
            "merchant": normalize_text(extracted_fields.get("merchant") or extracted_fields.get("vendor")),
            "notes": normalize_text(extracted_fields.get("notes") or extracted_fields.get("description")),
        },
        "line_items": extracted_fields.get("line_items") if isinstance(extracted_fields.get("line_items"), list) else [],
        "source_fields": extracted_fields,
    }
    return normalized


def validate_structured_document_fields(document: Dict[str, Any]) -> Dict[str, Any]:
    required_fields = ["document_type", "document_id", "date", "total"]
    errors: List[str] = []
    for field_name in required_fields:
        value = document.get(field_name)
        if value is None or value == "":
            errors.append(f"missing required field: {field_name}")
    return {"valid": not errors, "errors": errors, "document": document}
