from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyCategoryScore:
    category: str
    score: float
    severity: Optional[str] = None


@dataclass
class ModerationDecision:
    provider: str
    allowed: bool
    flagged: bool
    action: str
    categories: List[SafetyCategoryScore] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchModerationResult:
    results: List[ModerationDecision]


@dataclass
class RedactionResult:
    provider: str
    original_text: str
    redacted_text: str
    flagged: bool
    spans: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThresholdDecision:
    allowed: bool
    blocked_categories: List[str]
    observed_scores: Dict[str, float]


CATEGORY_NAME_MAP = {
    "hate": "hate",
    "hate/threatening": "hate/threatening",
    "harassment": "harassment",
    "harassment/threatening": "harassment/threatening",
    "self-harm": "self-harm",
    "self-harm/intent": "self-harm/intent",
    "self-harm/instructions": "self-harm/instructions",
    "sexual": "sexual",
    "sexual/minors": "sexual/minors",
    "violence": "violence",
    "violence/graphic": "violence/graphic",
}


def normalize_openai_categories(result: Dict[str, Any]) -> List[SafetyCategoryScore]:
    categories = result.get("categories") or {}
    scores = result.get("category_scores") or {}
    return [
        SafetyCategoryScore(
            category=CATEGORY_NAME_MAP.get(name, name),
            score=float(scores.get(name, 0.0) or 0.0),
            severity="flagged" if bool(flagged) else "safe",
        )
        for name, flagged in categories.items()
    ]


def decision_from_openai_result(result: Dict[str, Any], provider: str = "openai") -> ModerationDecision:
    categories = normalize_openai_categories(result)
    flagged = bool(result.get("flagged", False))
    return ModerationDecision(
        provider=provider,
        allowed=not flagged,
        flagged=flagged,
        action="block" if flagged else "allow",
        categories=categories,
        raw=result,
    )


def category_score_map(categories: List[SafetyCategoryScore]) -> Dict[str, float]:
    return {item.category: item.score for item in categories}
