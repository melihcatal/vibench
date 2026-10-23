# SAME-SCENARIO: safety_threshold.py
"""Apply per‑category thresholds to decide whether to allow text."""

from typing import Dict, Any

from moderate_text import moderate_text


def apply_thresholds(
    raw: Dict[str, Any], thresholds: Dict[str, float] = None
) -> Dict[str, Any]:
    """Return modified result with an overall decision based on thresholds.

    Args:
        raw: The raw moderation response from moderate_text.
        thresholds: Optional mapping of category name to min flag score required to block.

    Returns:
        The original dict with an added 'decision' field ('allow' or 'block').
    """
    if thresholds is None:
        thresholds = {
            "hate": 0.7,
            "self_harm": 0.6,
            "sexual": 0.5,
            "violence": 0.6,
        }
    # Default to allow
    decision = "allow"
    for cat, score in raw["raw"]["results"][0]["categories"].items():
        if score["flag"] >= thresholds.get(cat, 0.5):
            decision = "block"
            break
    raw["decision"] = decision
    return raw
