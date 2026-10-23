from typing import List, Dict, Any
from collections import defaultdict


def moderation_summary(decisions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Summarizes moderation decisions using aggregate statistics from Azure Content Moderator.
    """
    summary = {
        "total_messages": len(decisions),
        "allowed": 0,
        "blocked": 0,
        "violation_categories": defaultdict(int),
    }

    for decision in decisions:
        if decision.get("allow", True):
            summary["allowed"] += 1
        else:
            summary["blocked"] += 1
            for violation in decision.get("violations", []):
                summary["violation_categories"][violation["category"]] += 1

    summary["violation_categories"] = dict(summary["violation_categories"])
    return summary
