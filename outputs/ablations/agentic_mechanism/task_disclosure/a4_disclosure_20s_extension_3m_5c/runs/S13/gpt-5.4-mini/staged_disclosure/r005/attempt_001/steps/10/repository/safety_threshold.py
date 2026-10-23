import os
from dataclasses import dataclass
from typing import Dict, Mapping

import openai


DEFAULT_THRESHOLDS: Dict[str, float] = {
    "self_harm": 0.75,
    "violence": 0.80,
    "hate": 0.70,
    "sexual": 0.85,
}


@dataclass(frozen=True)
class SafetyDecision:
    allow: bool
    scores: Mapping[str, float]
    threshold_exceeded: str | None


def _score_text_with_openai(text: str) -> Dict[str, float]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    client = openai.OpenAI(api_key=api_key)
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    result = response.results[0]
    categories = result.categories
    scores = result.category_scores
    return {
        "self_harm": float(scores.self_harm),
        "violence": float(scores.violence),
        "hate": float(scores.hate),
        "sexual": float(scores.sexual),
        "self_harm_category": float(categories.self_harm),
        "violence_category": float(categories.violence),
        "hate_category": float(categories.hate),
        "sexual_category": float(categories.sexual),
    }


def allow_text(text: str, thresholds: Mapping[str, float] | None = None) -> SafetyDecision:
    active_thresholds = dict(DEFAULT_THRESHOLDS if thresholds is None else thresholds)
    scores = _score_text_with_openai(text)
    for category, threshold in active_thresholds.items():
        if scores.get(category, 0.0) >= threshold:
            return SafetyDecision(False, scores, category)
    return SafetyDecision(True, scores, None)
