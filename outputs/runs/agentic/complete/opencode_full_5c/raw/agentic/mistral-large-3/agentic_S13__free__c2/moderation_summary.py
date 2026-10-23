from typing import List, Dict
from collections import defaultdict


def summarize_moderation_decisions(decisions: List[Dict]) -> Dict:
    summary = defaultdict(int)

    for decision in decisions:
        if decision.get("allowed"):
            summary["allowed"] += 1
        else:
            summary["blocked"] += 1
            for category in decision.get("categories", []):
                summary[f"blocked_{category['name']}"] += 1

    return dict(summary)
