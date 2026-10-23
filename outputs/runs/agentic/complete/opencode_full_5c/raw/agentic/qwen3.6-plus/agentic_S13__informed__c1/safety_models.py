import os
from dataclasses import dataclass, field, asdict
from typing import Optional
from enum import Enum


class SafetyCategory(str, Enum):
    HATE = "hate"
    SELF_HARM = "self_harm"
    SEXUAL = "sexual"
    VIOLENCE = "violence"
    HARASSMENT = "harassment"


class ModerationDecision(str, Enum):
    ALLOW = "allow"
    FLAG = "flag"
    BLOCK = "block"


@dataclass
class CategoryScore:
    category: SafetyCategory
    score: float
    severity: str = "unknown"


@dataclass
class ModerationRequest:
    text: str
    user_id: Optional[str] = None
    context: Optional[str] = None
    categories: list[SafetyCategory] = field(
        default_factory=lambda: list(SafetyCategory)
    )


@dataclass
class ModerationResponse:
    text: str
    user_id: Optional[str]
    decision: ModerationDecision
    category_scores: list[CategoryScore]
    flagged_categories: list[SafetyCategory]
    raw_scores: dict[str, float]
    metadata: dict = field(default_factory=dict)


@dataclass
class BatchModerationRequest:
    messages: list[ModerationRequest]


@dataclass
class BatchModerationResponse:
    results: list[ModerationResponse]
    total: int
    flagged_count: int
    blocked_count: int


@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    flagged_spans: list[dict]
    decision: ModerationDecision


@dataclass
class ThresholdConfig:
    flag_threshold: float = 0.5
    block_threshold: float = 0.8
    category_overrides: dict[SafetyCategory, float] = field(default_factory=dict)

    def get_threshold(self, category: SafetyCategory, action: str) -> float:
        override = self.category_overrides.get(category)
        if override is not None:
            return override
        if action == "block":
            return self.block_threshold
        return self.flag_threshold


def load_threshold_config() -> ThresholdConfig:
    flag = float(os.environ.get("SAFETY_FLAG_THRESHOLD", "0.5"))
    block = float(os.environ.get("SAFETY_BLOCK_THRESHOLD", "0.8"))
    overrides_str = os.environ.get("SAFETY_CATEGORY_OVERRIDES", "")
    overrides = {}
    if overrides_str:
        for pair in overrides_str.split(","):
            cat, val = pair.strip().split(":")
            overrides[SafetyCategory(cat.strip())] = float(val.strip())
    return ThresholdConfig(
        flag_threshold=flag,
        block_threshold=block,
        category_overrides=overrides,
    )


def normalize_category_scores(raw_scores: dict) -> list[CategoryScore]:
    scores = []
    for cat_name, score in raw_scores.items():
        try:
            category = SafetyCategory(cat_name.lower())
        except ValueError:
            continue
        severity = "low"
        if score >= 0.8:
            severity = "high"
        elif score >= 0.5:
            severity = "medium"
        scores.append(
            CategoryScore(category=category, score=round(score, 4), severity=severity)
        )
    return scores


def determine_decision(
    category_scores: list[CategoryScore], thresholds: ThresholdConfig
) -> tuple[ModerationDecision, list[SafetyCategory]]:
    flagged = []
    blocked = []
    for cs in category_scores:
        if cs.score >= thresholds.get_threshold(cs.category, "block"):
            blocked.append(cs.category)
        elif cs.score >= thresholds.get_threshold(cs.category, "flag"):
            flagged.append(cs.category)
    if blocked:
        return ModerationDecision.BLOCK, blocked + flagged
    if flagged:
        return ModerationDecision.FLAG, flagged
    return ModerationDecision.ALLOW, []


def response_to_dict(response: ModerationResponse) -> dict:
    return {
        "text": response.text,
        "user_id": response.user_id,
        "decision": response.decision.value,
        "category_scores": [
            {"category": cs.category.value, "score": cs.score, "severity": cs.severity}
            for cs in response.category_scores
        ],
        "flagged_categories": [c.value for c in response.flagged_categories],
        "raw_scores": response.raw_scores,
        "metadata": response.metadata,
    }
