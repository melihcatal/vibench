import re
import json
from pathlib import Path


def validate_document_fields(document: dict) -> dict:
    """Validate required structured fields and confidence scores for an extracted document.

    Returns a dict with validation results: {
        "valid": bool,
        "missing_fields": list[str],
        "low_confidence": list[str]
    }
    """
    # Define required keys per document type
    required_by_type = {
        "invoice": {"vendor", "date", "total", "line_items"},
        "receipt": {"merchant", "tax", "total", "items"},
    }

    doc_type = document.get("type")
    if not doc_type or doc_type not in required_by_type:
        return {"valid": False, "missing_fields": ["type"], "low_confidence": []}

    missing = required_by_type[doc_type] - document.keys()
    # Simple confidence check placeholder: assume any field ending with _confidence < 0.8 is low
    low_conf = [
        k for k, v in document.items() if k.endswith("_confidence") and float(v) < 0.8
    ]

    return {
        "valid": len(missing) == 0,
        "missing_fields": list(missing),
        "low_confidence": low_conf,
    }
