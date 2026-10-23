from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyConfig:
    endpoint: str
    api_key: str
    project_id: Optional[str] = None
    threshold: float = 0.5


@dataclass
class ModerationRequest:
    text: str
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModerationDecision:
    allowed: bool
    category_scores: Dict[str, float] = field(default_factory=dict)
    redacted_text: Optional[str] = None
    reasons: List[str] = field(default_factory=list)


@dataclass
class BatchModerationResult:
    results: List[ModerationDecision] = field(default_factory=list)


@dataclass
class ThresholdRule:
    category: str
    max_score: float


@dataclass
class TranslatedAppeal:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class EmbeddingRecord:
    text: str
    vector: List[float]
    model: str


@dataclass
class AudioBrief:
    text: str
    audio_base64: str
    voice: str


def normalize_text(text: str) -> str:
    return " ".join((text or "").strip().split())
