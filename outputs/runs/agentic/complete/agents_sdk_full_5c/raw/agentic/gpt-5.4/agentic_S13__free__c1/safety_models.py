from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


CATEGORY_KEYS = [
    "hate",
    "sexual",
    "self_harm",
    "violence",
]


@dataclass
class SafetyCategoryScore:
    name: str
    severity: Optional[int] = None
    filtered: Optional[bool] = None


@dataclass
class SafetyDecision:
    text: str
    allowed: bool
    categories: Dict[str, SafetyCategoryScore] = field(default_factory=dict)
    provider: str = "azure_ai_content_safety"
    redacted_text: Optional[str] = None
    block_reasons: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchModerationResult:
    decisions: List[SafetyDecision]
    provider: str = "azure_ai_content_safety"


@dataclass
class SummaryResult:
    summary: str
    provider: str
    input_count: int


@dataclass
class TranslationResult:
    translated_text: str
    to_language: str
    provider: str


@dataclass
class EmbeddingResult:
    vector: List[float]
    dimensions: int
    provider: str


@dataclass
class AudioBriefResult:
    audio_base64: str
    format: str
    provider: str
    voice: str


def normalize_category_scores(raw_categories: List[Dict[str, Any]]) -> Dict[str, SafetyCategoryScore]:
    normalized: Dict[str, SafetyCategoryScore] = {}
    for item in raw_categories or []:
        name = str(item.get("category", "")).lower()
        if not name:
            continue
        normalized[name] = SafetyCategoryScore(
            name=name,
            severity=item.get("severity"),
            filtered=item.get("filtered"),
        )
    return normalized


def severity_map(categories: Dict[str, SafetyCategoryScore]) -> Dict[str, int]:
    result: Dict[str, int] = {}
    for key in CATEGORY_KEYS:
        score = categories.get(key)
        result[key] = 0 if score is None or score.severity is None else int(score.severity)
    return result
