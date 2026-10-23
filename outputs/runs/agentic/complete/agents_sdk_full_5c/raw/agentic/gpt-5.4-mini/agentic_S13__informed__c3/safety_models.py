from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class SafetyCategoryScore:
    category: str
    score: float
    severity: Optional[str] = None


@dataclass
class SafetyDecision:
    allowed: bool
    categories: List[SafetyCategoryScore] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModerationRequest:
    text: str
    language: Optional[str] = None
    context: Optional[str] = None


@dataclass
class BatchModerationRequest:
    messages: List[ModerationRequest]


@dataclass
class RedactionSpan:
    start: int
    end: int
    label: str


@dataclass
class ModerationResult:
    text: str
    decision: SafetyDecision
    redacted_text: Optional[str] = None
    spans: List[RedactionSpan] = field(default_factory=list)


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class EmbeddingRequest:
    texts: List[str]


@dataclass
class AudioBriefRequest:
    text: str
    voice: Optional[str] = None


def normalize_text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def normalize_categories(payload: Iterable[Mapping[str, Any]]) -> List[SafetyCategoryScore]:
    categories: List[SafetyCategoryScore] = []
    for item in payload:
        categories.append(
            SafetyCategoryScore(
                category=str(item.get("category") or item.get("name") or item.get("label") or "unknown"),
                score=float(item.get("score") or item.get("probability") or 0.0),
                severity=item.get("severity"),
            )
        )
    return categories
