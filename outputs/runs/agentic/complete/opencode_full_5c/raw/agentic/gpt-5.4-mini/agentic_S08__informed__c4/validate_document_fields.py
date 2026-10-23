from typing import Dict, Iterable, List, Tuple


def validate_document_fields(payload: Dict[str, object], required_fields: Iterable[str] = ("vendor", "date", "total"), min_confidence: float = 0.8) -> Tuple[bool, List[str]]:
    missing = []
    for field in required_fields:
        value = payload.get(field)
        if value in (None, "", []):
            missing.append(field)
    confidence = payload.get("confidence_scores", {})
    if isinstance(confidence, dict):
        for field in required_fields:
            score = confidence.get(field)
            if score is not None and score < min_confidence:
                missing.append(f"{field}:low_confidence")
    return (len(missing) == 0, missing)
