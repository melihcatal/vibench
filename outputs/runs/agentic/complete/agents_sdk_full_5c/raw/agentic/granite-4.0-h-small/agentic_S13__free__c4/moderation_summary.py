# moderation_summary.py
"""Summarize moderation decisions for downstream pipelines.
"""
from typing import List, Dict
from safety_models import SafetyResponse

def summarize(decisions: List[Dict[str, Any]]) -> Dict[str, int]:
    """Aggregate moderation outcomes.
    decisions: list of dicts as returned from moderate_text.py / moderate_batch.py.
    Returns counts of passed vs failed messages and overall unsafe flag presence."""
    summary = {
        "total": len(decisions),
        "passed": 0,
        "failed": 0,
        "unsafe_categories": []
    }
    for d in decisions:
        if d["passed"]:
            summary["passed"] += 1
        else:
            summary["failed"] += 1
            summary["unsafe_categories"].extend(d["flagged_categories"])
    # Deduplicate categories
    summary["unsafe_categories"] = list(set(summary["unsafe_categories"]))
    return summary
