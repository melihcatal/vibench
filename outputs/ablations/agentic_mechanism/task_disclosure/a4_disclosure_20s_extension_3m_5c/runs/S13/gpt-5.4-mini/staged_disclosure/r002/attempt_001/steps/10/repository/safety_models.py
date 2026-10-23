from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


@dataclass(frozen=True)
class TextSafetyRequest:
    text: str
    model: str = OPENAI_MODERATION_MODEL

    def to_payload(self) -> Dict[str, Any]:
        return {"model": self.model, "input": self.text}


@dataclass(frozen=True)
class TextSafetyResponse:
    flagged: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


DEFAULT_CATEGORY_THRESHOLDS: Dict[str, float] = {
    "harassment": 0.75,
    "harassment/threatening": 0.5,
    "hate": 0.75,
    "hate/threatening": 0.5,
    "self-harm": 0.5,
    "self-harm/intent": 0.25,
    "self-harm/instructions": 0.25,
    "sexual": 0.8,
    "sexual/minors": 0.01,
    "violence": 0.8,
    "violence/graphic": 0.5,
}


@dataclass(frozen=True)
class TextSafetyDecision:
    allowed: bool
    blocked_categories: Dict[str, float] = field(default_factory=dict)


def normalize_moderation_result(result: Mapping[str, Any]) -> TextSafetyResponse:
    return TextSafetyResponse(
        flagged=bool(result.get("flagged", False)),
        categories=dict(result.get("categories") or {}),
        category_scores=dict(result.get("category_scores") or {}),
        raw=dict(result),
    )


def normalize_moderation_payload(payload: Mapping[str, Any]) -> TextSafetyResponse:
    results = payload.get("results") or []
    first_result = results[0] if results else {}
    return normalize_moderation_result(first_result)


def evaluate_text_safety(
    scores: Mapping[str, float],
    thresholds: Optional[Mapping[str, float]] = None,
) -> TextSafetyDecision:
    merged_thresholds = dict(DEFAULT_CATEGORY_THRESHOLDS)
    if thresholds:
        merged_thresholds.update(thresholds)
    blocked_categories = {
        category: score
        for category, score in scores.items()
        if score >= merged_thresholds.get(category, 1.0)
    }
    return TextSafetyDecision(allowed=not blocked_categories, blocked_categories=blocked_categories)


def normalize_text_safety_response(
    payload: Mapping[str, Any],
    thresholds: Optional[Mapping[str, float]] = None,
) -> Dict[str, Any]:
    response = normalize_moderation_payload(payload)
    decision = evaluate_text_safety(response.category_scores, thresholds=thresholds)
    return {
        "flagged": response.flagged,
        "categories": response.categories,
        "category_scores": response.category_scores,
        "allowed": decision.allowed,
        "blocked_categories": decision.blocked_categories,
        "raw": response.raw,
    }
