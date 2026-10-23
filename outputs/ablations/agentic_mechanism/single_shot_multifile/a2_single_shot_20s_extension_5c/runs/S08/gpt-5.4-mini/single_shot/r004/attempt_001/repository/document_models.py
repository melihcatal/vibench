import json
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class DocumentExtractionRequest:
    document_type: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    valid: bool
    missing_fields: List[str]
    low_confidence_fields: List[str]
    score: float
    raw: Dict[str, Any] = field(default_factory=dict)


def parse_json_response(text: str) -> Dict[str, Any]:
    if not text:
        return {}
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        text = text[start : end + 1]
    return json.loads(text)


def normalize_expense_record(model_output: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
    try:
        parsed = parse_json_response(model_output)
    except Exception:
        parsed = {}
    normalized = dict(fallback)
    normalized.update(parsed)
    normalized.setdefault("source_type", fallback.get("document_type", "expense"))
    return normalized


def parse_validation_result(text: str) -> ValidationResult:
    data = parse_json_response(text)
    return ValidationResult(
        valid=bool(data.get("valid", False)),
        missing_fields=list(data.get("missing_fields", [])),
        low_confidence_fields=list(data.get("low_confidence_fields", [])),
        score=float(data.get("score", 0.0)),
        raw=data,
    )
