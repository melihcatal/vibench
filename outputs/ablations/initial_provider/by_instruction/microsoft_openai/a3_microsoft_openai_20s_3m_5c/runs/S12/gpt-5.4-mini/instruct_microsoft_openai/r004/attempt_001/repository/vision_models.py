from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class VisionRequest:
    image_path: str
    prompt: str
    model: str
    max_tokens: int = 300


@dataclass
class VisionResponse:
    text: str
    raw: Dict[str, Any]


def normalize_items(items: Any) -> List[str]:
    if items is None:
        return []
    if isinstance(items, str):
        return [items.strip()] if items.strip() else []
    if isinstance(items, list):
        result: List[str] = []
        for item in items:
            if isinstance(item, str):
                cleaned = item.strip()
                if cleaned:
                    result.append(cleaned)
            elif isinstance(item, dict):
                label = item.get("label") or item.get("name") or item.get("text") or item.get("caption")
                if isinstance(label, str) and label.strip():
                    result.append(label.strip())
        return result
    return [str(items)]


def normalize_text(value: Optional[Any]) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()
