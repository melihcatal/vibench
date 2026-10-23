from safety_models import get_default_thresholds
from typing import Dict, Any


def apply_safety_threshold(
    result: Dict[str, Any], custom_thresholds: Dict[str, float] = None
) -> Dict[str, Any]:
    """
    Applies category thresholds to decide whether to allow text.
    """
    thresholds = custom_thresholds or get_default_thresholds()
    violations = result.get("violations", [])
    blocked_categories = []
    max_severity = 0.0
    for violation in violations:
        label = violation.get("label")
        confidence = violation.get("confidence", 0.0)
        if confidence > thresholds.get(label, 0.5):
            blocked_categories.append(label)
        max_severity = max(max_severity, confidence)

    return {
        "allow": len(blocked_categories) == 0,
        "decision": "blocked" if blocked_categories else "allowed",
        "blocked_categories": blocked_categories,
        "max_confidence": max_severity,
    }
