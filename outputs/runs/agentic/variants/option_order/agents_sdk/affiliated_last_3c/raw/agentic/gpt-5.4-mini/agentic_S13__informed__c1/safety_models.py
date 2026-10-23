from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


@dataclass
class SafetyCategoryScore:
    category: str
    score: float
    threshold: float = 0.5

    def is_flagged(self) -> bool:
        return self.score >= self.threshold


@dataclass
class SafetyModerationRequest:
    text: str
    language: Optional[str] = None
    categories: Sequence[str] = field(default_factory=list)


@dataclass
class SafetyModerationDecision:
    flagged: bool
    category_scores: List[SafetyCategoryScore] = field(default_factory=list)
    provider: str = "azure-ai-content-safety"
    raw: Dict[str, Any] = field(default_factory=dict)

    def max_score(self) -> float:
        return max((c.score for c in self.category_scores), default=0.0)


@dataclass
class BatchModerationResult:
    decisions: List[SafetyModerationDecision]
    provider: str = "azure-ai-content-safety"


@dataclass
class RedactionResult:
    text: str
    spans: List[Tuple[int, int, str]] = field(default_factory=list)
    flagged: bool = False
    provider: str = "azure-ai-content-safety"


@dataclass
class ThresholdRule:
    category: str
    allow_threshold: float


@dataclass
class ThresholdDecision:
    allowed: bool
    reasons: List[str] = field(default_factory=list)
    provider: str = "azure-ai-content-safety"


@dataclass
class ModerationSummary:
    summary: str
    provider: str


@dataclass
class TranslationJob:
    text: str
    source_language: str
    target_language: str


@dataclass
class EmbeddingJob:
    text: str
    provider: str = "openai"


@dataclass
class AudioBriefRequest:
    text: str
    voice: str = "alloy"
    model: str = "gpt-4o-mini-tts"


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def clamp_score(score: Any) -> float:
    try:
        value = float(score)
    except (TypeError, ValueError):
        value = 0.0
    return max(0.0, min(1.0, value))


def decision_from_scores(scores: Mapping[str, Any], threshold: float = 0.5) -> SafetyModerationDecision:
    category_scores = [SafetyCategoryScore(category=k, score=clamp_score(v), threshold=threshold) for k, v in scores.items()]
    return SafetyModerationDecision(flagged=any(s.is_flagged() for s in category_scores), category_scores=category_scores)
