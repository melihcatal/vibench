from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ModerationRequest:
    text: str
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModerationDecision:
    allow: bool
    categories: Dict[str, float]
    rationale: str = ""
    redacted_text: Optional[str] = None


@dataclass
class BatchModerationResult:
    decisions: List[ModerationDecision]


@dataclass
class SafetyThresholds:
    thresholds: Dict[str, float] = field(default_factory=dict)


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_categories(categories: Dict[str, Any]) -> Dict[str, float]:
    normalized: Dict[str, float] = {}
    for key, value in categories.items():
        try:
            normalized[str(key)] = float(value)
        except (TypeError, ValueError):
            normalized[str(key)] = 0.0
    return normalized
