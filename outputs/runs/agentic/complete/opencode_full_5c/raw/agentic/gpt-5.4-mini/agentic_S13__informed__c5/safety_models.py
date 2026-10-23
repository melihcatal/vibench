from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ModerationCategory:
    name: str
    score: float
    flagged: bool = False


@dataclass
class ModerationRequest:
    text: str
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModerationResult:
    flagged: bool
    categories: List[ModerationCategory]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchModerationResult:
    results: List[ModerationResult]


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_thresholds(thresholds: Optional[Dict[str, float]]) -> Dict[str, float]:
    thresholds = thresholds or {}
    return {str(k): float(v) for k, v in thresholds.items()}
