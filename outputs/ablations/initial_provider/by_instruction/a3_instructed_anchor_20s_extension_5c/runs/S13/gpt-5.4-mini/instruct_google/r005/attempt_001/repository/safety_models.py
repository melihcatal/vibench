from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ModerationRequest:
    text: str
    categories: List[str] = field(default_factory=list)
    threshold: float = 0.5


@dataclass
class ModerationResult:
    allowed: bool
    category_scores: Dict[str, float] = field(default_factory=dict)
    reasons: List[str] = field(default_factory=list)
    redacted_text: Optional[str] = None
    raw_response: Any = None


@dataclass
class BatchModerationResult:
    results: List[ModerationResult]


@dataclass
class TranslationRequest:
    text: str
    source_language: str = "auto"
    target_language: str = "en"


@dataclass
class EmbeddingRequest:
    text: str


@dataclass
class AudioBriefRequest:
    text: str
    voice: str = "alloy"


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_scores(scores: Any) -> Dict[str, float]:
    if not isinstance(scores, dict):
        return {}
    return {str(k): float(v) for k, v in scores.items() if v is not None}
