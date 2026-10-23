from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def normalize_messages(payload: Dict[str, Any]) -> List[Dict[str, str]]:
    messages = payload.get('messages') or payload.get('items') or []
    normalized = []
    for item in messages:
        if isinstance(item, dict):
            normalized.append({'id': normalize_text(item.get('id')), 'text': normalize_text(item.get('text', item.get('content', '')))})
    return normalized


@dataclass
class ModerationDecision:
    allowed: bool
    severity: float
    category_scores: Dict[str, float]
    raw: Optional[Dict[str, Any]] = None
