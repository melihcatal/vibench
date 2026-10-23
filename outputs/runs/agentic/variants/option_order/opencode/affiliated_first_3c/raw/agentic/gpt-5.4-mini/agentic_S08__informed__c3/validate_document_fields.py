from typing import Any, Dict, List

from document_models import normalize_confidence


def validate_document_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    required = ["merchant_or_vendor", "transaction_date", "total_amount"]
    missing: List[str] = [name for name in required if not data.get(name)]
    confidence = normalize_confidence(data.get("confidence", 0.0))
    return {
        "valid": not missing and confidence >= 0.5,
        "missing": missing,
        "confidence": confidence,
    }
