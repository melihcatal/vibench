from __future__ import annotations

from typing import Any, Dict, Iterable

from document_models import ValidationResult


REQUIRED_FIELDS = {
    "invoice": ("vendor", "date", "total"),
    "receipt": ("merchant", "total"),
}


def validate_document_fields(document: Dict[str, Any], min_confidence: float = 0.75) -> Dict[str, Any]:
    doc = document.get("document")
    doc_type = getattr(doc, "document_type", "unknown")
    required = REQUIRED_FIELDS.get(doc_type, ())
    missing = [name for name in required if getattr(doc, name, None) in (None, "")]
    low_conf = []
    conf = getattr(doc, "confidence", None)
    if conf is None or conf < min_confidence:
        low_conf.append("confidence")
    result = ValidationResult(valid=not missing and not low_conf, missing_fields=missing, low_confidence_fields=low_conf)
    return {"validation": result, "provider": "amazon.bedrock-runtime", "model_id": None}
