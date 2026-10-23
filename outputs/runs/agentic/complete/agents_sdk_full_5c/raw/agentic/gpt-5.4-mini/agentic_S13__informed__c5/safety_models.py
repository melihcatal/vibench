from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyModerationRequest:
    text: str
    user_id: Optional[str] = None


@dataclass
class SafetyModerationResult:
    flagged: bool
    categories: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyBatchItem:
    text: str
    index: int
    user_id: Optional[str] = None


@dataclass
class SafetyBatchResult:
    items: List[SafetyModerationResult]


@dataclass
class SafetyThresholdConfig:
    thresholds: Dict[str, float]
    default_allow: bool = True


def normalize_text(text: str) -> str:
    return " ".join((text or "").strip().split())


def normalize_score_map(payload: Dict[str, Any]) -> Dict[str, float]:
    scores: Dict[str, float] = {}
    for key, value in payload.items():
        try:
            scores[str(key)] = float(value)
        except (TypeError, ValueError):
            continue
    return scores
