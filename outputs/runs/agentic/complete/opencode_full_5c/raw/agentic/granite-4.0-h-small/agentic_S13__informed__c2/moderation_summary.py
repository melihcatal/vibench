# [LATER-STEP] moderation_summary.py
"""Summarize moderation decisions across a set of messages.
Aggregates per‑category counts and produces a concise report.
"""


def summarize_decisions(decisions: list[dict]) -> dict:
    """Return a summary dict with category tallies and overall verdict."""
    summary = {"safe_count": 0, "unsafe_count": 0, "categories": {}}
    for d in decisions:
        label = d.get("label", "safe").lower()
        summary["categories"][label] = summary["categories"].get(label, 0) + 1
        if label != "safe":
            summary["unsafe_count"] += 1
        else:
            summary["safe_count"] += 1
    summary["overall"] = "safe" if summary["unsafe_count"] == 0 else "unsafe"
    return summary
