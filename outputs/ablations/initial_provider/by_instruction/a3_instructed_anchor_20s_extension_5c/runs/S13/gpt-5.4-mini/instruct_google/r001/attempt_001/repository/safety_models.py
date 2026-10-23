from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_messages(items: Any) -> List[str]:
    if not items:
        return []
    if isinstance(items, str):
        return [normalize_text(items)] if normalize_text(items) else []
    normalized: List[str] = []
    for item in items:
        text = normalize_text(item)
        if text:
            normalized.append(text)
    return normalized


@dataclass
class SafetyDecision:
    allowed: bool
    categories: Dict[str, float]
    raw: Optional[Dict[str, Any]] = None


@dataclass
class SafetyBatchDecision:
    decisions: List[SafetyDecision]
