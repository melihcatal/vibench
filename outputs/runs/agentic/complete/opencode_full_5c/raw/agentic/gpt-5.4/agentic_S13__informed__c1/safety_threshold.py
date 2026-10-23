from __future__ import annotations

from typing import Dict, Optional

from safety_client import get_default_thresholds


def apply_safety_thresholds(
    category_scores: Dict[str, float],
    thresholds: Optional[Dict[str, float]] = None,
) -> Dict[str, object]:
    active_thresholds = thresholds or get_default_thresholds()
    exceeded = {
        category: score
        for category, score in category_scores.items()
        if score >= float(active_thresholds.get(category, 0.5))
    }
    return {
        "allow": not bool(exceeded),
        "action": "allow" if not exceeded else "block",
        "exceeded_categories": exceeded,
        "thresholds": dict(active_thresholds),
    }
