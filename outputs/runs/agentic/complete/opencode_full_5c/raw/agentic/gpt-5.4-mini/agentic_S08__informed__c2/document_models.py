from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, Iterable, List


@dataclass
class InvoiceExtractionRequest:
    content: bytes
    content_type: str = "application/pdf"


@dataclass
class ReceiptExtractionRequest:
    content: bytes
    content_type: str = "application/pdf"


@dataclass
class ExpenseNormalizationRequest:
    raw_fields: Dict[str, Any]


@dataclass
class ValidationRequest:
    fields: Dict[str, Any]
    required_fields: List[str]
    minimum_confidence: float = 0.8


def normalize_text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def normalize_money(value: Any):
    if value in (None, ""):
        return None
    return str(Decimal(str(value)))


def standardize_expense_record(raw_fields: Dict[str, Any]) -> Dict[str, Any]:
    return {"vendor": normalize_text(raw_fields.get("vendor")), "date": normalize_text(raw_fields.get("date")), "total": normalize_money(raw_fields.get("total")), "currency": normalize_text(raw_fields.get("currency")), "line_items": raw_fields.get("line_items", []), "source": "azure-document-intelligence"}


def validate_required_fields(fields: Dict[str, Any], required_fields: Iterable[str], minimum_confidence: float) -> Dict[str, Any]:
    missing = [field for field in required_fields if field not in fields or fields[field] in (None, "")]
    confidence = {field: fields.get(f"{field}_confidence", 1.0) for field in required_fields}
    low = [field for field, score in confidence.items() if float(score) < minimum_confidence]
    return {"valid": not missing and not low, "missing": missing, "low_confidence": low, "confidence": confidence}
