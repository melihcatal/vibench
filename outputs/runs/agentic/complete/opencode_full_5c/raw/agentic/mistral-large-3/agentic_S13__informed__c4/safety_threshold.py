from typing import Dict, Optional
from safety_models import ModerationResponse


def apply_safety_threshold(
    response: ModerationResponse,
    category_thresholds: Optional[Dict[str, float]] = None,
    default_threshold: float = 0.5,
) -> bool:
    """Apply category thresholds to decide whether to allow text."""
    if not category_thresholds:
        category_thresholds = {
            "hate": 0.7,
            "violence": 0.8,
            "sexual": 0.6,
            "harassment": 0.7,
            "self_harm": 0.9,
        }

    for category, score in response.scores.items():
        threshold = category_thresholds.get(category, default_threshold)
        if score >= threshold:
            return False
    return True
