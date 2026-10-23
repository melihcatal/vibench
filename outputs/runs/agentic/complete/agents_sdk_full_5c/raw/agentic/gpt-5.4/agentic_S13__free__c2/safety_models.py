from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CategoryScore:
    name: str
    score: float
    flagged: bool = False


@dataclass
class ModerationResult:
    provider: str
    model: str
    flagged: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class RedactionResult:
    provider: str
    model: str
    original_text: str
    redacted_text: str
    flagged: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    spans: List[Dict[str, Any]] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class ThresholdDecision:
    allowed: bool
    blocked_categories: List[str]
    observed_scores: Dict[str, float]
    thresholds: Dict[str, float]


@dataclass
class BatchModerationResult:
    provider: str
    model: str
    results: List[ModerationResult]


DEFAULT_OPENAI_MODERATION_MODEL = "omni-moderation-latest"
DEFAULT_OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_OPENAI_TTS_MODEL = "gpt-4o-mini-tts"
DEFAULT_OPENAI_CHAT_MODEL = "gpt-4.1-mini"
DEFAULT_OPENAI_TRANSLATION_MODEL = "gpt-4.1-mini"


def normalize_openai_moderation_result(result: Any, model: str = DEFAULT_OPENAI_MODERATION_MODEL) -> ModerationResult:
    categories = dict(getattr(result, "categories", {}) or {})
    category_scores = dict(getattr(result, "category_scores", {}) or {})
    flagged = bool(getattr(result, "flagged", False))
    raw = {
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
    }
    return ModerationResult(
        provider="openai",
        model=model,
        flagged=flagged,
        categories=categories,
        category_scores=category_scores,
        raw=raw,
    )


def normalize_openai_moderation_response(response: Any, model: str = DEFAULT_OPENAI_MODERATION_MODEL) -> BatchModerationResult:
    results = [normalize_openai_moderation_result(item, model=model) for item in getattr(response, "results", [])]
    return BatchModerationResult(provider="openai", model=model, results=results)
