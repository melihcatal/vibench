from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class VisionImageInput:
    path: Optional[str] = None
    url: Optional[str] = None
    bytes_data: Optional[bytes] = None


def normalize_text_items(items: Any) -> List[str]:
    if items is None:
        return []
    if isinstance(items, str):
        return [items.strip()] if items.strip() else []
    result: List[str] = []
    for item in items:
        if isinstance(item, str):
            value = item.strip()
        elif isinstance(item, dict):
            value = str(
                item.get("name") or item.get("text") or item.get("label") or ""
            ).strip()
        else:
            value = str(item).strip()
        if value:
            result.append(value)
    return result


def build_response(
    provider: str,
    payload: Dict[str, Any],
    text: str = "",
    labels: Any = None,
    unsafe: Any = None,
) -> Dict[str, Any]:
    return {
        "provider": provider,
        "text": text,
        "labels": normalize_text_items(labels),
        "unsafe": bool(unsafe),
        "raw": payload,
    }
