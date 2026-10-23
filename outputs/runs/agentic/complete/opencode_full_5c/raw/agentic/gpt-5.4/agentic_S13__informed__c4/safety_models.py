from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SafetyRequest:
    text: str
    language: str | None = None
    user_id: str | None = None
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class CategoryScore:
    name: str
    score: float


@dataclass
class SafetyResult:
    provider: str
    text: str
    flagged: bool
    categories: dict[str, float]
    language: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchModerationResult:
    results: list[SafetyResult]


def normalize_text(value: str) -> str:
    return " ".join((value or "").split())


def normalize_scores(categories: dict[str, Any]) -> dict[str, float]:
    normalized: dict[str, float] = {}
    for key, value in categories.items():
        try:
            normalized[key.lower()] = float(value)
        except (TypeError, ValueError):
            continue
    return normalized


def result_to_dict(result: SafetyResult) -> dict[str, Any]:
    return {
        "provider": result.provider,
        "text": result.text,
        "flagged": result.flagged,
        "categories": result.categories,
        "language": result.language,
        "raw": result.raw,
    }
