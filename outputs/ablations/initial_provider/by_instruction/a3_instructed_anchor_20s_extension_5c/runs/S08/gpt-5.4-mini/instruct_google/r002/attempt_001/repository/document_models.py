from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ExtractionRequest:
    document_text: str
    document_type: str


@dataclass
class ExtractionResponse:
    fields: Dict[str, Any]
    confidence: float


def standardize_expense_record(fields: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "vendor": fields.get("vendor") or fields.get("merchant"),
        "date": fields.get("date"),
        "total": fields.get("total"),
        "tax": fields.get("tax"),
        "items": fields.get("items") or fields.get("line_items") or [],
    }


def validate_required_fields(fields: Dict[str, Any], required: List[str]) -> Dict[str, Any]:
    missing = [key for key in required if not fields.get(key)]
    return {"valid": not missing, "missing": missing}
