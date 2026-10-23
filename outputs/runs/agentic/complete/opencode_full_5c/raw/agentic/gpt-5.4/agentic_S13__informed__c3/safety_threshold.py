from __future__ import annotations

from typing import Dict

from safety_client import analyze_text
from safety_models import SafetyRequest, scores_to_dict


DEFAULT_THRESHOLDS = {
    "toxicity": 0.75,
    "severe_toxicity": 0.6,
    "insult": 0.8,
    "profanity": 0.9,
    "threat": 0.4,
    "identity_attack": 0.5,
}


def apply_safety_threshold(
    text: str, thresholds: Dict[str, float] | None = None, language: str = "en"
) -> Dict[str, object]:
    result = analyze_text(SafetyRequest(text=text, language=language))
    threshold_map = thresholds or DEFAULT_THRESHOLDS
    scores = scores_to_dict(result.categories)
    exceeded = {
        name: scores.get(name, 0.0)
        for name, limit in threshold_map.items()
        if scores.get(name, 0.0) >= limit
    }
    return {
        "provider": "Perspective API",
        "model": "commentanalyzer-v1alpha1",
        "allow": not bool(exceeded),
        "scores": scores,
        "thresholds": threshold_map,
        "exceeded": exceeded,
    }
