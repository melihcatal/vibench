"""Define local request, response, and normalization helpers for Text Content Safety.

Provides data classes and utilities for working with OpenAI Moderation API responses.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ModerationRequest:
    """Request payload for OpenAI text moderation.

    Uses text-moderation-latest model on api.openai.com.
    """
    input: Any
    model: str = "text-moderation-latest"

    def to_dict(self) -> Dict[str, Any]:
        return {"model": self.model, "input": self.input}


@dataclass
class ModerationResponse:
    """Normalized moderation response with per-category scores."""
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    model: str
    provider: str = "openai"
    provider_endpoint: str = "api.openai.com"
    thresholds_applied: Optional[Dict[str, float]] = None
    exceeded_categories: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "flagged": self.flagged,
            "categories": self.categories,
            "category_scores": self.category_scores,
            "model": self.model,
            "provider": self.provider,
            "provider_endpoint": self.provider_endpoint,
            "thresholds_applied": self.thresholds_applied,
            "exceeded_categories": self.exceeded_categories or [],
        }


@dataclass
class BatchModerationResponse:
    """Batch moderation response with per-message results."""
    results: List[Dict[str, Any]]
    total: int
    flagged_count: int
    model: str
    provider: str = "openai"
    provider_endpoint: str = "api.openai.com"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "results": self.results,
            "total": self.total,
            "flagged_count": self.flagged_count,
            "model": self.model,
            "provider": self.provider,
            "provider_endpoint": self.provider_endpoint,
        }


@dataclass
class RedactionRequest:
    """Request payload for redaction-based moderation."""
    input: str
    model: str = "text-moderation-latest"
    redact_token: str = "[REDACTED]"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "input": self.input,
            "redact_token": self.redact_token,
        }


@dataclass
class RedactionResponse:
    """Response from unsafe text redaction."""
    original_text: str
    redacted_text: str
    flagged_categories: List[str]
    category_scores: Dict[str, float]
    was_modified: bool
    model: str
    provider: str = "openai"
    provider_endpoint: str = "api.openai.com"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_text": self.original_text,
            "redacted_text": self.redacted_text,
            "flagged_categories": self.flagged_categories,
            "category_scores": self.category_scores,
            "was_modified": self.was_modified,
            "model": self.model,
            "provider": self.provider,
            "provider_endpoint": self.provider_endpoint,
        }


def normalize_openai_categories(
    raw_categories: Any,
    as_float: bool = False,
) -> Dict[str, Any]:
    """Normalize OpenAI moderation categories into a flat dict.

    Converts the Pydantic BaseModel categories or category_scores returned by
    openai.moderations.create into a standard Python dict with snake_case keys
    suitable for downstream processing.

    Args:
        raw_categories: The categories or category_scores object from OpenAI response.
        as_float: If True, convert values to float (for scores). Otherwise use bool (for flags).

    Returns:
        Dict mapping category names to their values.
    """
    normalized: Dict[str, Any] = {}
    for key, value in raw_categories.model_dump().items():
        normalized[key] = float(value) if as_float else bool(value)
    return normalized
