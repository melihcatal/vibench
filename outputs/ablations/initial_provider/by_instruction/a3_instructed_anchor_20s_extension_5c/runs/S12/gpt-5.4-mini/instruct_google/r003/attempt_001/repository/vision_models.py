from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_label_annotations(items: List[Dict[str, Any]]) -> List[str]:
    return [item.get("description", "") for item in items if item.get("description")]


def normalize_text_annotations(items: List[Dict[str, Any]]) -> str:
    if not items:
        return ""
    return items[0].get("description", "")


def normalize_safe_search(result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "adult": result.get("adult", "UNKNOWN"),
        "spoof": result.get("spoof", "UNKNOWN"),
        "medical": result.get("medical", "UNKNOWN"),
        "violence": result.get("violence", "UNKNOWN"),
        "racy": result.get("racy", "UNKNOWN"),
    }


@dataclass
class VisionResult:
    provider: str
    data: Any
