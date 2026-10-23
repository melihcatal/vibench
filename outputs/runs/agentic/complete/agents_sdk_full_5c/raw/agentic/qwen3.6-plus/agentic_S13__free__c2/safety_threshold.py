"""
safety_threshold.py - Applies category thresholds to decide whether to allow text.

Uses the OpenAI Moderation API (api.openai.com) with the text-moderation-latest model
and applies configurable per-category thresholds to determine content allow/deny decisions.
"""

import os
import openai


SAFETY_CATEGORIES = [
    "hate",
    "hate/threatening",
    "harassment",
    "harassment/threatening",
    "self-harm",
    "self-harm/intent",
    "self-harm/instructions",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
]

DEFAULT_THRESHOLDS = {
    "hate": 0.3,
    "hate/threatening": 0.1,
    "harassment": 0.3,
    "harassment/threatening": 0.1,
    "self-harm": 0.2,
    "self-harm/intent": 0.1,
    "self-harm/instructions": 0.05,
    "sexual": 0.4,
    "sexual/minors": 0.01,
    "violence": 0.3,
    "violence/graphic": 0.2,
}


def _get_moderation_client():
    """Create an OpenAI moderation client using the official SDK."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = openai.OpenAI(api_key=api_key)
    return client


def apply_safety_threshold(
    text: str,
    thresholds: dict = None,
    strict_mode: bool = False,
) -> dict:
    """
    Apply category-specific thresholds to decide whether to allow text.

    Args:
        text: The user text to evaluate.
        thresholds: Dict of category -> threshold score. Uses defaults if not provided.
        strict_mode: If True, any category exceeding its threshold denies the text.
                     If False, only high-severity categories (minors, threatening, instructions)
                     trigger automatic denial.

    Returns:
        Dictionary with:
            - allowed: bool indicating if text passes all thresholds
            - category_scores: dict of category -> score
            - exceeded_thresholds: list of categories where score >= threshold
            - decision: 'allow' or 'deny'
            - provider: openai
    """
    client = _get_moderation_client()
    effective_thresholds = thresholds or DEFAULT_THRESHOLDS.copy()

    result = client.moderations.create(
        input=text,
        model="text-moderation-latest",
    )

    moderation = result.results[0]
    category_scores = {}
    exceeded_thresholds = []
    high_severity_exceeded = []

    high_severity_categories = {
        "hate/threatening",
        "harassment/threatening",
        "self-harm/intent",
        "self-harm/instructions",
        "sexual/minors",
        "violence/graphic",
    }

    for category in SAFETY_CATEGORIES:
        threshold = effective_thresholds.get(category, DEFAULT_THRESHOLDS.get(category, 0.5))
        score = getattr(moderation.category_scores, category, 0.0)
        category_scores[category] = score

        if score >= threshold:
            exceeded_thresholds.append(category)
            if category in high_severity_categories:
                high_severity_exceeded.append(category)

    if strict_mode:
        allowed = len(exceeded_thresholds) == 0
    else:
        allowed = len(high_severity_exceeded) == 0

    return {
        "allowed": allowed,
        "decision": "allow" if allowed else "deny",
        "category_scores": category_scores,
        "exceeded_thresholds": exceeded_thresholds,
        "high_severity_exceeded": high_severity_exceeded,
        "strict_mode": strict_mode,
        "model": "text-moderation-latest",
        "provider": "openai",
        "provider_endpoint": "api.openai.com/v1/moderations",
    }


def check_text_allowance(text: str, custom_thresholds: dict = None) -> bool:
    """
    Simple boolean check: is this text allowed under the given thresholds?

    Args:
        text: The user text to evaluate.
        custom_thresholds: Optional custom threshold overrides.

    Returns:
        True if text is allowed, False otherwise.
    """
    result = apply_safety_threshold(text, thresholds=custom_thresholds, strict_mode=True)
    return result["allowed"]


def get_threshold_recommendation(text: str) -> dict:
    """
    Get threshold-based recommendation with reasoning for content review.

    Args:
        text: The user text to evaluate.

    Returns:
        Recommendation dict with allow/deny decision and detailed reasoning.
    """
    result = apply_safety_threshold(text, strict_mode=False)

    if result["allowed"]:
        recommendation = "approve"
        reasoning = "No high-severity categories exceeded thresholds."
    elif result["high_severity_exceeded"]:
        recommendation = "deny"
        reasoning = f"High-severity violations detected: {result['high_severity_exceeded']}"
    else:
        recommendation = "flag_for_review"
        reasoning = f"Moderate violations detected but no high-severity issues: {result['exceeded_thresholds']}"

    return {
        "recommendation": recommendation,
        "reasoning": reasoning,
        "decision": result["decision"],
        "exceeded_thresholds": result["exceeded_thresholds"],
        "provider": "openai",
    }


if __name__ == "__main__":
    import sys
    sample_text = sys.argv[1] if len(sys.argv) > 1 else "Testing content moderation thresholds."
    result = apply_safety_threshold(sample_text, strict_mode=True)
    print(f"Decision: {result['decision']}")
    if result["exceeded_thresholds"]:
        print(f"Exceeded: {result['exceeded_thresholds']}")
