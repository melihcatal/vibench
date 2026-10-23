from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class VisionImageRequest:
    image_path: str
    prompt: str
    language: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisionResult:
    provider: str
    content: str
    raw: Dict[str, Any]
    labels: List[str] = field(default_factory=list)
    texts: List[str] = field(default_factory=list)
    safety: Optional[str] = None


def normalize_labels(items: Any) -> List[str]:
    if not items:
        return []
    out = []
    for item in items:
        if isinstance(item, str):
            out.append(item.strip())
        elif isinstance(item, dict):
            value = item.get("label") or item.get("name") or item.get("text")
            if value:
                out.append(str(value).strip())
    return out


def normalize_texts(items: Any) -> List[str]:
    if not items:
        return []
    out = []
    for item in items:
        if isinstance(item, str):
            out.append(item.strip())
        elif isinstance(item, dict):
            value = item.get("text") or item.get("value")
            if value:
                out.append(str(value).strip())
    return out
