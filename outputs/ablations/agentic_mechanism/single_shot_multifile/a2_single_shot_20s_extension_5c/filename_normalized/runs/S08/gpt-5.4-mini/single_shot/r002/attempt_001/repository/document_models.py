import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentExtractionRequest:
    document_type: str
    text: str
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    confidence_threshold: float = 0.0
    extra_context: Dict[str, Any] = field(default_factory=dict)

    def to_prompt(self, *, schema_name: str) -> str:
        payload = {
            "document_type": self.document_type,
            "schema_name": schema_name,
            "file_name": self.file_name,
            "mime_type": self.mime_type,
            "confidence_threshold": self.confidence_threshold,
            "text": self.text,
            "extra_context": self.extra_context,
        }
        return json.dumps(payload, ensure_ascii=False)


def normalize_document_text(text: str) -> str:
    return " ".join((text or "").split())


def normalize_expense_record(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "source": extracted_fields.get("provider", "unknown"),
        "document_type": extracted_fields.get("document_type", "expense"),
        "merchant": extracted_fields.get("vendor") or extracted_fields.get("merchant"),
        "date": extracted_fields.get("date"),
        "currency": extracted_fields.get("currency", "USD"),
        "total": extracted_fields.get("total"),
        "tax": extracted_fields.get("tax"),
        "items": extracted_fields.get("line_items") or extracted_fields.get("items") or [],
        "confidence": extracted_fields.get("confidence", 0.0),
    }


def validate_extracted_document(payload: Dict[str, Any]) -> Dict[str, Any]:
    required = ["document_type", "confidence"]
    missing: List[str] = [key for key in required if key not in payload or payload.get(key) in (None, "")]
    confidence = payload.get("confidence", 0.0)
    valid = not missing and isinstance(confidence, (int, float)) and confidence >= 0.0
    return {"valid": valid, "missing": missing, "confidence": confidence, "payload": payload}
