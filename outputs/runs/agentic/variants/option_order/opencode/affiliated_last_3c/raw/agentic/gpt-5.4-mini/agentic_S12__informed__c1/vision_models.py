from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ImageInput:
    image_url: Optional[str] = None
    image_path: Optional[str] = None
    image_bytes: Optional[bytes] = None


@dataclass
class VisionResult:
    provider: str
    content: Any
    raw: Dict[str, Any]


def normalize_labels(items: Any) -> List[str]:
    if not items:
        return []
    out: List[str] = []
    for item in items:
        if isinstance(item, str):
            out.append(item)
        elif isinstance(item, dict):
            name = item.get("name") or item.get("label") or item.get("description")
            if name:
                out.append(str(name))
    return out


def normalize_text(items: Any) -> str:
    if isinstance(items, str):
        return items
    if not items:
        return ""
    if isinstance(items, list):
        parts = []
        for item in items:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(str(item.get("text") or item.get("description") or ""))
        return " ".join(p for p in parts if p)
    return str(items)


def normalize_safety_score(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {"unsafe": bool(value)}
