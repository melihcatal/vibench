from typing import Any, Dict, List


def normalize_moderation_result(result: Dict[str, Any]) -> Dict[str, Any]:
    return result


def normalize_batch_moderation_result(result: Dict[str, Any]) -> Dict[str, Any]:
    return result


def normalize_redaction_result(result: Dict[str, Any]) -> Dict[str, Any]:
    return result


def evaluate_thresholds(scores: Dict[str, Any], thresholds: Dict[str, float]) -> Dict[str, Any]:
    categories = scores.get("categories", scores)
    flagged = False
    reasons: List[str] = []
    for category, threshold in thresholds.items():
        value = categories.get(category)
        if isinstance(value, bool):
            if value and threshold <= 1.0:
                flagged = True
                reasons.append(category)
        elif isinstance(value, (int, float)) and value >= threshold:
            flagged = True
            reasons.append(category)
    return {"allow": not flagged, "flagged_categories": reasons, "scores": scores}
