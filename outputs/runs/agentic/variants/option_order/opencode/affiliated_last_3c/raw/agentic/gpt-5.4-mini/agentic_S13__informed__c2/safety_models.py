from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyRequest:
    text: str
    categories: List[str] = field(default_factory=list)
    locale: Optional[str] = None


@dataclass
class SafetyDecision:
    allowed: bool
    scores: Dict[str, float] = field(default_factory=dict)
    labels: List[str] = field(default_factory=list)
    redacted_text: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def normalize_categories(categories: Any) -> List[str]:
    if not categories:
        return []
    return [normalize_text(item).lower() for item in categories if normalize_text(item)]
