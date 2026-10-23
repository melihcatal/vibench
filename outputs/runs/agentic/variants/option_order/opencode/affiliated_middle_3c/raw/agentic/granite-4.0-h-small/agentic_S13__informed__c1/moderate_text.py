# [SAME-SCENARIO] moderate_text.py
# Scores user text for unsafe or policy-violating content

from safety_client import TextSafetyClient


def score_text(user_text: str, **kwargs) -> dict:
    """Send a single text to the configured safety service and return a score/response.

    Args:
        user_text: The user-provided text to evaluate.
        **kwargs: Additional parameters forwarded to the underlying client (e.g., thresholds).

    Returns:
        A dict containing at least the keys:
            - "unsafe": bool indicating policy violation
            - "reason": brief rationale string
            - "score": numeric risk score (if provided by provider)
    """
    client = TextSafetyClient()
    response = client.analyze(user_text, **kwargs)
    # Normalize response to a common format
    return {
        "unsafe": response.get("unsafe", False),
        "reason": response.get("reason", "No unsafe content detected."),
        "score": response.get("score"),
    }
