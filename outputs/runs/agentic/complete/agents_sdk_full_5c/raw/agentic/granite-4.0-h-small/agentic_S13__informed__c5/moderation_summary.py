# moderation_summary.py
import os
import json
from safety_client import TextSafetyClient


def summarize_moderations(decisions: list[dict]) -> dict:
    """Aggregates per-message moderation decisions into a concise summary.
    Returns a dict with counts of allowed/block, overall distribution per
    category, and optionally a list of problematic items for review. """
    summary = {
        "total": len(decisions),
        "allowed": 0,
        "blocked": 0,
        "categories": {
            "hate": 0,
            "self_harm": 0,
            "sexual": 0,
            "violence": 0
        },
        "problematic_items": []  # messages flagged as block
    }
    client = TextSafetyClient()  # Reuse the same client for optional extra details
    for entry in decisions:
        raw = entry.get("raw")
        moderation = entry.get("moderation", {})
        decision = moderation.get("decision")
        summary[decision] += 1
        # Increment category counts (only where scores are available)
        for cat, score in moderation.get("scores", {}).items():
            if score is not None:
                summary["categories"][cat] += 1
        # Collect details for blocked items (with scores for context)
        if decision == "block":
            summary["problematic_items"].append({
                "message": raw.get("content") if raw else None,
                "scores": moderation.get("scores")
            })
    return summary

if __name__ == "__main__":
    # Example usage – assume `decisions` comes from moderate_batch.py
    mock_decisions = [
        {
            "decision": "allow",
            "raw": {
                "content": "This is fine."
            }
        },
        {
            "decision": "block",
            "raw": {
                "content": "You are a terrible person."
            }
        }
    ]
    print(summarize_moderations(mock_decisions))