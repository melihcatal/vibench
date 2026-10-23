from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional


@dataclass
class SafetyRequest:
    text: str
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyDecision:
    label: str
    score: float
    categories: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_unsafe(self) -> bool:
        return self.label.lower() not in {"allow", "safe", "non-violent"} and self.score > 0


@dataclass
class ModerationResult:
    request: SafetyRequest
    decision: SafetyDecision


@dataclass
class RedactionSpan:
    start: int
    end: int
    category: str
    score: float


@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    spans: List[RedactionSpan] = field(default_factory=list)
    decision: Optional[SafetyDecision] = None


@dataclass
class ThresholdRule:
    category: str
    threshold: float


@dataclass
class ThresholdDecision:
    allowed: bool
    triggered: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchModerationResult:
    results: List[ModerationResult]


@dataclass
class ModerationSummary:
    total: int
    unsafe: int
    details: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class EmbeddingRequest:
    texts: List[str]


@dataclass
class TTSRequest:
    text: str
    voice: Optional[str] = None
    language: Optional[str] = None


@dataclass
class NormalizedCategoryScores:
    scores: Dict[str, float] = field(default_factory=dict)


def normalize_scores(scores: Mapping[str, Any]) -> Dict[str, float]:
    normalized: Dict[str, float] = {}
    for key, value in scores.items():
        try:
            normalized[str(key)] = float(value)
        except (TypeError, ValueError):
            continue
    return normalized


def coerce_texts(texts: Iterable[str]) -> List[str]:
    return [str(t) for t in texts if t is not None]
