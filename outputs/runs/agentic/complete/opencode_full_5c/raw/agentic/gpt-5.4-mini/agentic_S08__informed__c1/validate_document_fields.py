from typing import Any, Dict, List

from document_client import merge_confidence


def validate_document_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    required = ["vendor", "date", "total"]
    missing = [field for field in required if not data.get(field)]
    confidence = merge_confidence(
        data.get("confidence"),
        *(
            item.get("confidence")
            for item in data.get("items", [])
            if isinstance(item, dict)
        ),
    )
    return {
        "valid": not missing and confidence >= 0.5,
        "missing": missing,
        "confidence": confidence,
    }
