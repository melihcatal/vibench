from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ImageAnalysisRequest:
    image_path: str
    language: Optional[str] = None
    prompt: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ImageAnalysisResponse:
    provider: str
    result: Any
    raw: Any


def normalize_text_items(items: Any) -> List[str]:
    if items is None:
        return []
    if isinstance(items, str):
        return [items]
    normalized: List[str] = []
    for item in items:
        if isinstance(item, str):
            normalized.append(item)
        elif isinstance(item, dict):
            for key in ("text", "description", "label", "value", "name"):
                if item.get(key):
                    normalized.append(str(item[key]))
                    break
        else:
            normalized.append(str(item))
    return normalized


def join_text(items: Any) -> str:
    return ", ".join(normalize_text_items(items))


def pick_first_present(
    data: Dict[str, Any], keys: List[str], default: Any = None
) -> Any:
    for key in keys:
        if key in data and data[key] is not None:
            return data[key]
    return default
