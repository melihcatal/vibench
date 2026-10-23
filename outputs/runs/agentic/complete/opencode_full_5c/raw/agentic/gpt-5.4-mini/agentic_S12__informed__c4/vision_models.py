from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class VisionImageRequest:
    image_path: str
    language: Optional[str] = None
    max_results: Optional[int] = None


@dataclass
class VisionTextRequest:
    image_path: str


@dataclass
class VisionSafetyRequest:
    image_path: str


def normalize_list(items: Any) -> List[str]:
    if not items:
        return []
    if isinstance(items, list):
        return [str(item) for item in items if item is not None]
    return [str(items)]


def normalize_label_response(labels: Any) -> Dict[str, Any]:
    return {"labels": normalize_list(labels)}


def normalize_description_response(description: Any) -> Dict[str, Any]:
    return {"description": "" if description is None else str(description)}


def normalize_text_response(text: Any) -> Dict[str, Any]:
    return {"text": "" if text is None else str(text)}


def normalize_safety_response(result: Any) -> Dict[str, Any]:
    if isinstance(result, dict):
        return result
    return {"safety": str(result)}
