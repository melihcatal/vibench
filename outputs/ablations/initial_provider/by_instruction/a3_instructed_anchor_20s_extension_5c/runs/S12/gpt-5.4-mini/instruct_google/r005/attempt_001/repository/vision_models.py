from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def image_reference(path: str) -> Dict[str, str]:
    return {"path": path}


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_labels(items: Any) -> List[str]:
    if not items:
        return []
    labels: List[str] = []
    for item in items:
        if isinstance(item, str):
            text = item.strip()
        elif isinstance(item, dict):
            text = normalize_text(item.get("description") or item.get("label") or item.get("text"))
        else:
            text = normalize_text(item)
        if text:
            labels.append(text)
    return labels


@dataclass
class VisionResult:
    labels: List[str]
    text: str = ""
    description: str = ""
    safety: str = "unknown"
