from typing import Dict, List


def validate_document_fields(
    extracted: Dict, required: List[str] | None = None, min_confidence: float = 0.8
) -> Dict:
    required = required or ["vendor", "date", "total"]
    missing = [field for field in required if not extracted.get(field)]
    confidence = float(extracted.get("confidence", 0.0))
    return {
        "valid": not missing and confidence >= min_confidence,
        "missing": missing,
        "confidence": confidence,
    }
