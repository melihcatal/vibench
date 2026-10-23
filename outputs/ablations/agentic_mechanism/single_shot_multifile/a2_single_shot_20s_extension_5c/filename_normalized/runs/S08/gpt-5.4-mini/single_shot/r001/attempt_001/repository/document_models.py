import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ExtractRequest:
    document_type: str
    text: str
    document_id: Optional[str] = None
    extra_context: Dict[str, Any] = field(default_factory=dict)

    def to_prompt(self) -> str:
        payload = {
            "document_type": self.document_type,
            "document_id": self.document_id,
            "text": self.text,
            "extra_context": self.extra_context,
        }
        return json.dumps(payload, ensure_ascii=False)


@dataclass
class ExtractionResult:
    data: Dict[str, Any]

    @classmethod
    def from_json(cls, raw: str) -> "ExtractionResult":
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {"raw": raw}
        return cls(data=parsed)


def normalize_invoice_output(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "vendor": data.get("vendor") or data.get("merchant"),
        "date": data.get("date") or data.get("invoice_date"),
        "total": data.get("total") or data.get("total_amount"),
        "line_items": data.get("line_items") or data.get("items") or [],
        "currency": data.get("currency"),
        "confidence": data.get("confidence"),
        "raw": data,
    }


def normalize_receipt_output(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "merchant": data.get("merchant") or data.get("vendor"),
        "tax": data.get("tax") or data.get("tax_amount"),
        "total": data.get("total") or data.get("total_amount"),
        "items": data.get("items") or data.get("line_items") or [],
        "currency": data.get("currency"),
        "confidence": data.get("confidence"),
        "raw": data,
    }


def normalize_expense_record(extracted_fields: Dict[str, Any], source: Optional[str] = None) -> str:
    payload = {
        "source": source,
        "document": extracted_fields,
        "target_schema": {
            "vendor": "string",
            "transaction_date": "string",
            "total_amount": "number",
            "currency": "string",
            "tax_amount": "number",
            "items": "array",
            "notes": "string",
            "confidence": "number",
        },
    }
    return json.dumps(payload, ensure_ascii=False)


def validation_prompt(document_payload: Dict[str, Any]) -> str:
    return json.dumps({"document_payload": document_payload}, ensure_ascii=False)
