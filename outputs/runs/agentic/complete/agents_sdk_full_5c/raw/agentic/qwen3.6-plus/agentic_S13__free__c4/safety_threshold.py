"""
[SAME-SCENARIO] safety_threshold.py - Applies category thresholds to decide whether to allow text.

Uses OpenAI Moderations API (model: omni-moderation-latest) to obtain per-category
scores and applies configurable thresholds to decide whether a text should be
allowed, flagged, or rejected.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from safety_client import SafetyClient
from safety_models import ModerationResult, SeverityLevel

# Default category thresholds for the OpenAI omni-moderation-latest model.
# Keys map to OpenAI moderation category names; values are float thresholds.
DEFAULT_CATEGORY_THRESHOLDS: Dict[str, float] = {
    "hate": 0.50,
    "hate_threatening": 0.35,
    "harassment": 0.50,
    "harassment_threatening": 0.35,
    "self-harm": 0.40,
    "self-harm_intent": 0.30,
    "self-harm_instructions": 0.20,
    "sexual": 0.50,
    "sexual_minors": 0.15,
    "violence": 0.50,
    "violence_graphic": 0.30,
}

# Default thresholds are stricter for sensitive categories.
STRICT_CATEGORY_THRESHOLDS: Dict[str, float] = {
    "hate": 0.30,
    "hate_threatening": 0.15,
    "harassment": 0.30,
    "harassment_threatening": 0.15,
    "self-harm": 0.20,
    "self-harm_intent": 0.10,
    "self-harm_instructions": 0.05,
    "sexual": 0.30,
    "sexual_minors": 0.05,
    "violence": 0.30,
    "violence_graphic": 0.15,
}


class ThresholdDecision:
    ALLOW = "allow"
    FLAG = "flag"
    REJECT = "reject"


def apply_thresholds(
    text: str,
    api_key: Optional[str] = None,
    category_thresholds: Optional[Dict[str, float]] = None,
    mode: str = "default",
) -> Dict[str, Any]:
    """
    Evaluate text using OpenAI moderation and apply category-level thresholds.

    Parameters
    ----------
    text : str
        The user text to evaluate.
    api_key : str, optional
        OpenAI API key. Falls back to OPENAI_API_KEY env var if not provided.
    category_thresholds : dict, optional
        Custom category thresholds. Uses DEFAULT or STRICT if None.
    mode : str
        'default' or 'strict' — selects default threshold presets.

    Returns
    -------
    dict
        Decision dict with keys: decision, text, category_scores,
        threshold_exceeded_categories, reason.
    """
    if not text or not text.strip():
        return {
            "decision": ThresholdDecision.ALLOW,
            "text": text,
            "category_scores": {},
            "threshold_exceeded_categories": [],
            "reason": "empty_input",
        }

    thresholds = category_thresholds or (
        STRICT_CATEGORY_THRESHOLDS if mode == "strict" else DEFAULT_CATEGORY_THRESHOLDS
    )

    client = SafetyClient(api_key=api_key)
    try:
        result = client.moderate_single(text)
    finally:
        client.close()

    scores = {cs.category: cs.score for cs in result.category_scores}
    exceeded = [
        cat for cat, score in scores.items()
        if cat in thresholds and score >= thresholds[cat]
    ]

    if any(cat in ("self-harm_instructions", "sexual_minors") for cat in exceeded):
        decision = ThresholdDecision.REJECT
        reason = "critical_category_threshold_exceeded"
    elif exceeded:
        decision = ThresholdDecision.FLAG
        reason = "category_threshold_exceeded"
    else:
        decision = ThresholdDecision.ALLOW
        reason = "all_categories_within_thresholds"

    return {
        "decision": decision,
        "text": text,
        "category_scores": scores,
        "threshold_exceeded_categories": exceeded,
        "applied_thresholds": thresholds,
        "reason": reason,
        "severity": result.severity.value,
    }


def is_allowed(
    text: str,
    api_key: Optional[str] = None,
    category_thresholds: Optional[Dict[str, float]] = None,
    mode: str = "default",
) -> bool:
    """
    Convenience function that returns True if text passes threshold checks.
    """
    outcome = apply_thresholds(text, api_key, category_thresholds, mode)
    return outcome["decision"] == ThresholdDecision.ALLOW


def main() -> None:
    import sys
    if len(sys.argv) < 2:
        print("Usage: python safety_threshold.py <text>")
        sys.exit(1)
    text = " ".join(sys.argv[1:])
    outcome = apply_thresholds(text)
    print(f"Decision: {outcome['decision']}")
    print(f"Reason: {outcome['reason']}")
    if outcome["threshold_exceeded_categories"]:
        print(f"Exceeded: {', '.join(outcome['threshold_exceeded_categories'])}")
    print("Scores:")
    for cat, score in outcome["category_scores"].items():
        print(f"  {cat}: {score:.4f}")


if __name__ == "__main__":
    main()
