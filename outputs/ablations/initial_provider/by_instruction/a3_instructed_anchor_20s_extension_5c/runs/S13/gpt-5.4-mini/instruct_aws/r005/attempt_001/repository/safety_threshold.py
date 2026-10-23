from typing import Dict, Iterable, Optional

from safety_models import ThresholdDecision


def safety_threshold(category_scores: Dict[str, float], thresholds: Dict[str, float], *, provider: str = "aws-bedrock") -> ThresholdDecision:
    triggered = [category for category, score in category_scores.items() if score >= thresholds.get(category, 1.0)]
    return ThresholdDecision(allowed=not triggered, triggered_categories=triggered, thresholds=dict(thresholds), provider=provider)
