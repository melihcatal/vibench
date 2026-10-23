from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyCategoryScore:
    category: str
    score: float
    threshold: float = 0.5
    flagged: bool = False


@dataclass
class SafetyDecision:
    allowed: bool
    categories: List[SafetyCategoryScore] = field(default_factory=list)
    rationale: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_text(text: Any) -> str:
    return "" if text is None else str(text).strip()


def normalize_messages(messages: Any) -> List[str]:
    if messages is None:
        return []
    if isinstance(messages, str):
        return [normalize_text(messages)]
    return [normalize_text(message) for message in messages]


def normalize_thresholds(thresholds: Optional[Dict[str, Any]]) -> Dict[str, float]:
    if not thresholds:
        return {}
    return {str(key): float(value) for key, value in thresholds.items()}
