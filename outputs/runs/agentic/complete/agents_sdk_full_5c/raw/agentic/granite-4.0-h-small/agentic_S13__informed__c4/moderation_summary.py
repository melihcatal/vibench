import json
from typing import List, Dict
from safety_models import ModerationResponse, CategoryScore, UnsafeSpan

def create_summary(responses: List[ModerationResponse]) -> dict:
    """Summarizes moderation decisions across a batch of texts.

    Returns a dict with counts per category and overall safe/unsafe flag.
    """
    summary = {
        "total": len(responses),
        "unsafe_count": 0,
        "category_counts": {},
        "unsafe_spans": []
    }
    for resp in responses:
        # Evaluate overall unsafe: if any category score exceeds threshold
        overall_safe = True
        for cat in resp.categories:
            if cat.score > 0.5:  # simple threshold
                overall_safe = False
                summary["unsafe_count"] += 1
                summary["category_counts"].setdefault(cat.category, 0)
                summary["category_counts"][cat.category] += 1
        if not overall_safe:
            # Collect unsafe spans from each response (stubbed; assume none)
            for span in resp.raw.get('unsafe_spans', []):
                summary['unsafe_spans'].append(span)
    return summary
