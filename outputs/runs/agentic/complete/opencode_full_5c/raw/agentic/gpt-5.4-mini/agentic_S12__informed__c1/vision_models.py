from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_image_input(image: Any) -> str:
    if isinstance(image, bytes):
        return image.decode("utf-8")
    return str(image)


def normalize_text_list(items: Any) -> List[str]:
    if items is None:
        return []
    if isinstance(items, list):
        return [str(item) for item in items if str(item).strip()]
    return [str(items)]


@dataclass
class VisionRequest:
    image: str
    prompt: Optional[str] = None
    language: Optional[str] = None


@dataclass
class VisionResponse:
    provider: str
    result: Dict[str, Any]
