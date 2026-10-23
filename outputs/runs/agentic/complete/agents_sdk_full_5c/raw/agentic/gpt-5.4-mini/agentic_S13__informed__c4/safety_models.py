from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class SafetyModerationRequest:
    text: str
    categories: Optional[List[str]] = None
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyModerationResult:
    flagged: bool
    category_scores: Dict[str, float] = field(default_factory=dict)
    category_flags: Dict[str, bool] = field(default_factory=dict)
    provider_raw: Any = None
    redacted_text: Optional[str] = None
    rationale: Optional[str] = None


@dataclass
class ModerationDecision:
    allowed: bool
    flagged: bool
    reason: str
    scores: Dict[str, float] = field(default_factory=dict)


@dataclass
class ModerationBatchItem:
    index: int
    text: str
    decision: ModerationDecision


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class EmbeddingRequest:
    text: str
    model: Optional[str] = None


@dataclass
class AudioBriefRequest:
    text: str
    voice: Optional[str] = None
    language: Optional[str] = None


def normalize_scores(scores: Mapping[str, Any]) -> Dict[str, float]:
    normalized: Dict[str, float] = {}
    for key, value in scores.items():
        try:
            normalized[key] = float(value)
        except (TypeError, ValueError):
            continue
    return normalized


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def chunk_texts(texts: Iterable[str]) -> List[str]:
    return [normalize_text(text) for text in texts]
