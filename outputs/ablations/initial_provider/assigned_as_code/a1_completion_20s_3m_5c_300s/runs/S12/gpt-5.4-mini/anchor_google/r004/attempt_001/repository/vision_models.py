from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def image_bytes_from_payload(payload: Dict[str, Any]) -> bytes:
    data = payload.get("image_bytes")
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode("utf-8")
    raise ValueError("payload must include image_bytes")


def normalize_labels(items: List[Any]) -> List[Dict[str, Any]]:
    return [{"name": getattr(item, "description", ""), "confidence": getattr(item, "score", 0.0)} for item in items]


def normalize_text_annotations(items: List[Any]) -> List[str]:
    return [getattr(item, "description", "") for item in items if getattr(item, "description", "")]


def normalize_safe_search(result: Any) -> Dict[str, Any]:
    return {
        "adult": getattr(result, "adult", None),
        "spoof": getattr(result, "spoof", None),
        "medical": getattr(result, "medical", None),
        "violence": getattr(result, "violence", None),
        "racy": getattr(result, "racy", None),
    }


@dataclass
class VisionRequest:
    image_bytes: bytes
    config: Optional[Dict[str, Any]] = None


@dataclass
class VisionResponse:
    data: Dict[str, Any]
