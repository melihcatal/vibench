# LATER-STEP: moderation_summary.py
"""Summarize moderation decisions for monitoring / reporting.
"""
from typing import List, Dict

from safety_models import normalize_moderation_response
from safety_client import get_moderation_client


def summarize_decisions(results: List[Dict[str, Any]]) -> Dict[str, int]:
    """Aggregate counts of allowed vs blocked and most severe flag.

    Args:
        results: List of dicts returned by each moderation call (raw + decision fields).

    Returns:
        Dictionary with summary statistics.
    """
    summary = {
        "allowed": 0,
        "blocked": 0,
        "most_severe_flag": None,
        "most_severe_score": 0.0,
    }
    for entry in results:
        if entry["decision"] == "block":
            summary["blocked"] += 1
            # Gather all flagged categories from the raw response
            for hit in entry["raw"]["results"][0]["flagged_content"]:
                cat = hit["category"]
                score = hit["score"]
                if (summary["most_severe_score"] is None)
                or (score > summary["most_severe_score"]):
                    summary["most_severe_flag"] = cat
                    summary["most_severe_score"] = score
        else:
            summary["allowed"] += 1
    return summary
