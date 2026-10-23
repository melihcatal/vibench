from typing import Dict, Any, Optional


def apply_safety_threshold(
    moderation_result: Dict[str, Any],
    thresholds: Dict[str, int]
) -> Dict[str, Any]:
    """
    Apply category thresholds to decide whether to allow text.
    Uses Azure AI Content Safety severity levels (0-7).
    """
    decision = {
        "allow": True,
        "blocked_categories": [],
        "scores": moderation_result
    }

    if moderation_result.get("hate", 0) >= thresholds.get("hate", 0):
        decision["allow"] = False
        decision["blocked_categories"].append("hate")

    if moderation_result.get("self_harm", 0) >= thresholds.get("self_harm", 0):
        decision["allow"] = False
        decision["blocked_categories"].append("self_harm")

    if moderation_result.get("sexual", 0) >= thresholds.get("sexual", 0):
        decision["allow"] = False
        decision["blocked_categories"].append("sexual")

    if moderation_result.get("violence", 0) >= thresholds.get("violence", 0):
        decision["allow"] = False
        decision["blocked_categories"].append("violence")

    return decision