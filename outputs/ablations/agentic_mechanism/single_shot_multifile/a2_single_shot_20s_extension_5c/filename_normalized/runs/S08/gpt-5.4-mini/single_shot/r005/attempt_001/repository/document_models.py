import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentExtractionRequest:
    document_text: str
    task_name: str
    instructions: str
    model: Optional[str] = None
    schema_name: Optional[str] = None


@dataclass
class ExtractionResult:
    data: Dict[str, Any] = field(default_factory=dict)
    raw: Optional[Any] = None

    @classmethod
    def from_openai_response(cls, response: Any) -> "ExtractionResult":
        text = getattr(response, "output_text", None)
        if not text and hasattr(response, "output"):
            text = json.dumps(response.output)
        parsed: Dict[str, Any]
        try:
            parsed = json.loads(text or "{}")
        except Exception:
            parsed = {"raw_text": text or ""}
        return cls(data=parsed, raw=response)

    def to_dict(self) -> Dict[str, Any]:
        return self.data


def coerce_text_payload(document: Any) -> str:
    if document is None:
        return ""
    if isinstance(document, str):
        return document
    if isinstance(document, bytes):
        return document.decode("utf-8", errors="ignore")
    if isinstance(document, dict):
        return json.dumps(document, ensure_ascii=False)
    return str(document)


def normalize_expense_record(extracted: Dict[str, Any]) -> Dict[str, Any]:
    vendor = extracted.get("vendor") or extracted.get("merchant")
    total = extracted.get("total")
    currency = extracted.get("currency") or extracted.get("currency_code")
    line_items = extracted.get("line_items") or extracted.get("items") or []
    return {
        "vendor_name": vendor,
        "transaction_date": extracted.get("date") or extracted.get("transaction_date"),
        "total_amount": total,
        "currency": currency,
        "line_items": line_items,
        "notes": extracted.get("notes") or extracted.get("memo"),
        "source": extracted,
    }


def validate_document_structure(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            payload = {"raw_text": payload}
    required = ["vendor", "date", "total"]
    missing: List[str] = [k for k in required if not payload.get(k)]
    confidence = payload.get("confidence", {}) if isinstance(payload, dict) else {}
    low_confidence = [k for k, v in confidence.items() if isinstance(v, (int, float)) and v < 0.7]
    return {
        "valid": not missing and not low_confidence,
        "missing_fields": missing,
        "low_confidence_fields": low_confidence,
        "payload": payload,
    }
