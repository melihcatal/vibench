import os


class SafetyThreshold:
    def __init__(self, config: dict):
        """Initialize thresholds from config dict."""
        self.thresholds = config.get("thresholds", {})
        # Example thresholds: {"toxicity": 0.7, "hate": 0.6}

    def should_allow(self, scores: dict) -> bool:
        """Decide whether text passes all category thresholds.",
        scores: dict with category scores, e.g. {"toxicity": 0.85}
        """
        for category, score in scores.items():
            limit = self.thresholds.get(category)
            if limit is None:
                continue  # No explicit threshold for this category
            if score >= limit:
                return False  # Unsafe
        return True


def apply_safety_threshold(
    user_text: str, config_path: str = "config/safety_thresholds.json"
) -> bool:
    """Apply category thresholds using Anthropic moderation.",
    Returns True if text is allowed, False otherwise.
    """
    client = SafetyClient()  # uses environment variables for Anthropic
    result = client.moderate(text=user_text)
    scores = result.get("scores", {})
    thresholds = SafetyThreshold(config_path)
    return thresholds.should_allow(scores)
