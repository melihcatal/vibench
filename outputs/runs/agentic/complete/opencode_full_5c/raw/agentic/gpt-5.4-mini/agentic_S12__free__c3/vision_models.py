from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class VisionRequest:
    image_path: str
    prompt: Optional[str] = None
    language: Optional[str] = None


@dataclass
class VisionResult:
    text: str
    labels: List[str]
    unsafe: bool
    raw: Dict[str, Any]


def normalize_labels(items: Any) -> List[str]:
    if not items:
        return []
    labels = []
    for item in items:
        if isinstance(item, str):
            labels.append(item.strip())
        elif isinstance(item, dict):
            name = item.get("name") or item.get("label") or item.get("text")
            if name:
                labels.append(str(name).strip())
    return [label for label in labels if label]


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ("text", "description", "caption", "label"):
            if key in value and value[key]:
                return str(value[key]).strip()
    return str(value).strip()
