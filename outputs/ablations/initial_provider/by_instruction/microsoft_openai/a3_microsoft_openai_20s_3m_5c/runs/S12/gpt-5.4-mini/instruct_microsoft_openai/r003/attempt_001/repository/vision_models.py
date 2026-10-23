from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class VisionResult:
    text: str
    items: List[str]
    raw: Optional[Dict[str, Any]] = None


def normalize_items(items: Any) -> List[str]:
    if items is None:
        return []
    if isinstance(items, list):
        out = []
        for item in items:
            if isinstance(item, str):
                value = item.strip()
                if value:
                    out.append(value)
            elif isinstance(item, dict):
                value = str(item.get("name") or item.get("label") or item.get("text") or "").strip()
                if value:
                    out.append(value)
        return out
    if isinstance(items, str):
        return [part.strip() for part in items.split(",") if part.strip()]
    return [str(items).strip()]


def build_result(text: str, items: Any = None, raw: Optional[Dict[str, Any]] = None) -> VisionResult:
    return VisionResult(text=text.strip(), items=normalize_items(items), raw=raw)
