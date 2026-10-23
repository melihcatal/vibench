from __future__ import annotations

from typing import Dict, Optional

from safety_client import AzureContentSafetyClient


DEFAULT_THRESHOLDS: Dict[str, float] = {
    "sexual": 0.4,
    "hate": 0.4,
    "violence": 0.5,
    "self_harm": 0.3,
}


def safety_threshold(scores: Dict[str, float], thresholds: Optional[Dict[str, float]] = None, client: Optional[AzureContentSafetyClient] = None) -> bool:
    client = client or AzureContentSafetyClient()
    thresholds = thresholds or DEFAULT_THRESHOLDS
    payload = client.threshold(scores, thresholds)
    return bool(payload.get("allowed", False))


def apply_thresholds(scores: Dict[str, float]) -> Dict[str, bool]:
    return {category: score <= DEFAULT_THRESHOLDS.get(category, 1.0) for category, score in scores.items()}
