from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, MutableMapping, Optional


@dataclass
class TextSafetyRequest:
    text: str
    categories: List[str] = field(default_factory=list)
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TextSafetyDecision:
    allowed: bool
    scores: Dict[str, float] = field(default_factory=dict)
    labels: Dict[str, bool] = field(default_factory=dict)
    provider: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchSafetyResponse:
    decisions: List[TextSafetyDecision]


@dataclass
class RedactionSpan:
    start: int
    end: int
    label: str
    replacement: str = "[REDACTED]"


@dataclass
class RedactionResult:
    text: str
    spans: List[RedactionSpan] = field(default_factory=list)
    decision: Optional[TextSafetyDecision] = None


@dataclass
class ModerationSummary:
    summary: str
    counts: Dict[str, int] = field(default_factory=dict)
    provider: str = ""


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    provider: str = ""


@dataclass
class EmbeddingResult:
    vector: List[float]
    provider: str = ""
    model: str = ""


@dataclass
class AudioBrief:
    audio_path: Optional[str]
    text: str
    provider: str = ""


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def as_dict(mapping: Mapping[str, Any] | MutableMapping[str, Any]) -> Dict[str, Any]:
    return dict(mapping)
