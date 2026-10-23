from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ImageRequest:
    image_path: str
    prompt: Optional[str] = None
    language: Optional[str] = None


@dataclass
class ImageLabel:
    name: str
    confidence: float


@dataclass
class ImageTextBlock:
    text: str
    confidence: float


@dataclass
class SafetyResult:
    unsafe: bool
    categories: List[str]
    raw: Dict[str, Any]


def normalize_labels(items: Any) -> List[ImageLabel]:
    out: List[ImageLabel] = []
    for item in items or []:
        name = item.get("name") or item.get("label") or item.get("description") or ""
        confidence = float(item.get("confidence", item.get("score", 0.0)) or 0.0)
        out.append(ImageLabel(name=name, confidence=confidence))
    return out


def normalize_text_blocks(items: Any) -> List[ImageTextBlock]:
    out: List[ImageTextBlock] = []
    for item in items or []:
        text = item.get("text") or item.get("description") or ""
        confidence = float(item.get("confidence", item.get("score", 0.0)) or 0.0)
        out.append(ImageTextBlock(text=text, confidence=confidence))
    return out
