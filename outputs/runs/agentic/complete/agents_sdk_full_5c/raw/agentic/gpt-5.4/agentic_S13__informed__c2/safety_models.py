from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


DEFAULT_CATEGORY_MAP: Dict[str, str] = {
    "TOXICITY": "toxicity",
    "SEVERE_TOXICITY": "severe_toxicity",
    "INSULT": "insult",
    "PROFANITY": "profanity",
    "THREAT": "threat",
    "IDENTITY_ATTACK": "identity_attack",
    "SEXUALLY_EXPLICIT": "sexually_explicit",
    "FLIRTATION": "flirtation",
}


@dataclass
class SafetyRequest:
    text: str
    language: Optional[str] = None
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CategoryScore:
    category: str
    score: float
    raw_name: Optional[str] = None


@dataclass
class SafetyResponse:
    text: str
    scores: List[CategoryScore]
    flagged: bool
    provider: str
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def score_map(self) -> Dict[str, float]:
        return {item.category: item.score for item in self.scores}


@dataclass
class BatchModerationResult:
    text: str
    flagged: bool
    categories: Dict[str, float]
    provider: str
    raw_response: Dict[str, Any] = field(default_factory=dict)


def normalize_attribute_name(attribute_name: str) -> str:
    return DEFAULT_CATEGORY_MAP.get(attribute_name, attribute_name.lower())


def perspective_scores_from_response(response_json: Dict[str, Any]) -> List[CategoryScore]:
    attribute_scores = response_json.get("attributeScores", {})
    scores: List[CategoryScore] = []
    for raw_name, payload in attribute_scores.items():
        summary = payload.get("summaryScore", {})
        value = float(summary.get("value", 0.0))
        scores.append(
            CategoryScore(
                category=normalize_attribute_name(raw_name),
                score=value,
                raw_name=raw_name,
            )
        )
    return scores


def flagged_from_thresholds(scores: List[CategoryScore], thresholds: Dict[str, float]) -> bool:
    for item in scores:
        threshold = thresholds.get(item.category)
        if threshold is not None and item.score >= threshold:
            return True
    return False


def categories_dict(scores: List[CategoryScore]) -> Dict[str, float]:
    return {score.category: score.score for score in scores}
