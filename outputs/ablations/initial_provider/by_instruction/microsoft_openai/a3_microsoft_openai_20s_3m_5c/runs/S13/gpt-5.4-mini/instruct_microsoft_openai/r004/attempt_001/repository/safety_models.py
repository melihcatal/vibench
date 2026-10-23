from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _to_text(value: Any) -> str:
    return "" if value is None else str(value)


def normalize_text(text: Any) -> str:
    return _to_text(text).strip()


@dataclass
class ModerationDecision:
    flagged: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchModerationResult:
    results: List[ModerationDecision]


@dataclass
class RedactionSpan:
    start: int
    end: int
    label: str


@dataclass
class RedactionResult:
    text: str
    spans: List[RedactionSpan] = field(default_factory=list)
    flagged: bool = False


@dataclass
class ThresholdResult:
    allowed: bool
    triggered: List[str] = field(default_factory=list)
    scores: Dict[str, float] = field(default_factory=dict)


@dataclass
class SummaryResult:
    summary: str


@dataclass
class TranslationResult:
    text: str


@dataclass
class EmbeddingResult:
    vector: List[float]


@dataclass
class AudioBriefResult:
    audio_b64: str
