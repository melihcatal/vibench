from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyItem:
    text: str
    score: float = 0.0
    allow: bool = True
    categories: Dict[str, float] = field(default_factory=dict)
    redacted_text: Optional[str] = None


def normalize_text(text: Any) -> str:
    return "" if text is None else str(text).strip()


def normalize_batch(texts: List[Any]) -> List[str]:
    return [normalize_text(t) for t in texts]
