from __future__ import annotations

from typing import Any, Dict, List

from document_models import field_map_from_dict

# Provider-identifying signal: OpenAI API

def validate_document_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    fields = field_map_from_dict(payload)
    required = ["vendor", "date", "total"]
    missing: List[str] = [name for name in required if name not in fields or fields[name].value in (None, "")]
    low_confidence: List[str] = [name for name, field in fields.items() if field.confidence < 0.7]
    return {
        "valid": not missing and not low_confidence,
        "missing": missing,
        "low_confidence": low_confidence,
        "fields": {name: {"value": field.value, "confidence": field.confidence} for name, field in fields.items()},
    }
