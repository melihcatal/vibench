from typing import List, Dict
from safety_models import ModerationDecision, SafetyCategory


def summarize_moderation_decisions(decisions: List[ModerationDecision]) -> Dict[str, int]:
    """
    Summarizes moderation decisions using counts of allowed/blocked content.
    """
    summary = {"allowed": 0, "blocked": 0}
    category_counts = {category.value: 0 for category in SafetyCategory}

    for decision in decisions:
        if decision["allowed"]:
            summary["allowed"] += 1
        else:
            summary["blocked"] += 1
            for category, blocked in decision["categories"].items():
                if blocked:
                    category_counts[category.value] += 1

    summary["categories"] = category_counts
    return summary