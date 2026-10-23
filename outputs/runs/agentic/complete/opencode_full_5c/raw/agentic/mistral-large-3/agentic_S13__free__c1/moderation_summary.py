from typing import List, Dict


def summarize_moderation_decisions(decisions: List[Dict]) -> Dict:
    summary = {
        "total_messages": len(decisions),
        "allowed": 0,
        "blocked": 0,
        "flagged_categories": {},
    }

    for decision in decisions:
        if decision["is_allowed"]:
            summary["allowed"] += 1
        else:
            summary["blocked"] += 1
            for category in decision.get("flagged_categories", []):
                if category not in summary["flagged_categories"]:
                    summary["flagged_categories"][category] = 0
                summary["flagged_categories"][category] += 1

    return summary
