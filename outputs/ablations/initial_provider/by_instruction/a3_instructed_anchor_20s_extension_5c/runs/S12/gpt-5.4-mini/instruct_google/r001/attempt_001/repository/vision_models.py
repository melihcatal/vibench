from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class VisionResult:
    labels: List[str]
    description: Optional[str] = None
    text: Optional[str] = None
    safety: Optional[Dict[str, Any]] = None


def normalize_labels(items: Any) -> List[str]:
    out: List[str] = []
    if not items:
        return out
    for item in items:
        if isinstance(item, str):
            value = item.strip()
        else:
            value = str(item).strip()
        if value and value not in out:
            out.append(value)
    return out


def ensure_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()
