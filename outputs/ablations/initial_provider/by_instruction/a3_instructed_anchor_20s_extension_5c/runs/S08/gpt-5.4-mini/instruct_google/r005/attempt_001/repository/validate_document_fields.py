from typing import Any, Dict, List

from document_client import load_config


def validate_document_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    load_config()
    required = ["vendor", "date", "total"]
    missing: List[str] = [field for field in required if not data.get(field)]
    low_confidence = [
        field
        for field in required
        if isinstance(data.get(field), dict) and data[field].get("confidence", 0.0) < 0.8
    ]
    return {"valid": not missing and not low_confidence, "missing": missing, "low_confidence": low_confidence}
