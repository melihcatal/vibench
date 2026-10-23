from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_categories(value: Any) -> Dict[str, float]:
    if not isinstance(value, dict):
        return {}
    result: Dict[str, float] = {}
    for key, item in value.items():
        try:
            result[str(key)] = float(item)
        except (TypeError, ValueError):
            continue
    return result


@dataclass
class ModerationRequest:
    text: str
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModerationDecision:
    allowed: bool
    flagged: bool
    categories: Dict[str, float]
    category_applied_thresholds: Dict[str, float]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchModerationRequest:
    messages: List[ModerationRequest]


@dataclass
class BatchModerationResponse:
    decisions: List[ModerationDecision]
