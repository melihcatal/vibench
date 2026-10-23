from __future__ import annotations

from typing import Dict, Iterable, Sequence

from safety_client import SafetyClient
from safety_models import ThresholdRule, normalize_category_scores, threshold_allows

DEFAULT_RULES: Sequence[ThresholdRule] = (
    ThresholdRule(category="Hate", threshold=0.6),
    ThresholdRule(category="SelfHarm", threshold=0.4),
    ThresholdRule(category="Sexual", threshold=0.7),
    ThresholdRule(category="Violence", threshold=0.8),
)


def apply_thresholds(scores: Dict[str, float], rules: Sequence[ThresholdRule] = DEFAULT_RULES) -> bool:
    return threshold_allows(scores, rules)


def moderate_with_threshold(text: str, rules: Sequence[ThresholdRule] = DEFAULT_RULES) -> bool:
    client = SafetyClient()
    try:
        raw = client.moderate_text(text)
        scores = normalize_category_scores(raw.get("categories", raw))
        return apply_thresholds(scores, rules)
    finally:
        client.close()
