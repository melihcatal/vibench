from typing import Dict, List


def validate_document_fields(fields: Dict[str, object]) -> Dict[str, List[str]]:
    missing = [name for name in ("vendor", "date", "total") if not fields.get(name)]
    low_confidence = []
    confidence = (
        fields.get("confidence", {})
        if isinstance(fields.get("confidence", {}), dict)
        else {}
    )
    for key in ("vendor", "date", "total"):
        score = confidence.get(key)
        if score is not None and score < 0.8:
            low_confidence.append(key)
    return {"missing": missing, "low_confidence": low_confidence}
