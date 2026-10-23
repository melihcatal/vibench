from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ModerationRequest:
    text: str
    language: str | None = None
    user_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CategoryScore:
    name: str
    score: float
    flagged: bool


@dataclass
class ModerationResult:
    text: str
    action: str
    blocked: bool
    categories: dict[str, CategoryScore]
    provider: str
    raw: dict[str, Any]


@dataclass
class RedactionSpan:
    start: int
    end: int
    label: str
    replacement: str = "[REDACTED]"


@dataclass
class BatchModerationResult:
    results: list[ModerationResult]
    provider: str


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def moderation_result_to_dict(result: ModerationResult) -> dict[str, Any]:
    payload = asdict(result)
    payload["categories"] = {
        name: asdict(category) for name, category in result.categories.items()
    }
    return payload


def batch_result_to_dict(batch: BatchModerationResult) -> dict[str, Any]:
    return {
        "provider": batch.provider,
        "results": [moderation_result_to_dict(result) for result in batch.results],
    }
