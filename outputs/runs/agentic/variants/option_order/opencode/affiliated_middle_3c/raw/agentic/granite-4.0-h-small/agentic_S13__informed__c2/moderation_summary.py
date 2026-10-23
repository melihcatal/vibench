from typing import List, Any
from safety_models import SafetyResponse


def summarize_moderation(decisions: List[SafetyResponse]) -> dict:
    """Aggregates per‑message moderation results into a concise summary.

    Returns a dict containing:
    - total_messages
    - unsafe_count
    - unsafe_examples (up to 5)
    - category_counts (e.g., {"TOXICITY": 3, "SEVERE_TOXICITY": 1})
    """
    total = len(decisions)
    unsafe = [d for d in decisions if any(v >= 0.5 for v in d["scores"].values())]
    summary = {
        "total_messages": total,
        "unsafe_count": len(unsafe),
        "unsafe_examples": [
            {"text": d["text"], "unsafe_categories": list(d["scores"].keys())}
            for d in unsafe[:5]
        ],
        "category_counts": {},
    }
    for d in decisions:
        for cat, score in d["scores"].items():
            summary["category_counts"][cat] = summary["category_counts"].get(cat, 0) + 1
    return summary
