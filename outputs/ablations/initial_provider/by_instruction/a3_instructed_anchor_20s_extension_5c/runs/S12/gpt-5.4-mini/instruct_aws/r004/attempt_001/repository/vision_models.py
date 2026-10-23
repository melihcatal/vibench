from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class VisionImageInput:
    image_path: str
    image_bytes: Optional[bytes] = None
    source_uri: Optional[str] = None


@dataclass
class VisionResult:
    provider: str
    kind: str
    source: str
    data: Dict[str, Any]


def normalize_labels(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(items, key=lambda item: float(item.get("confidence", 0.0)), reverse=True)


def normalize_text(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(items, key=lambda item: float(item.get("confidence", 0.0)), reverse=True)


def normalize_safety(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(items, key=lambda item: float(item.get("confidence", 0.0)), reverse=True)
