from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ImageAnalysisRequest:
    image_path: str
    mime_type: str = "image/jpeg"
    language_hints: Optional[List[str]] = None
    max_results: int = 10


@dataclass
class LabelResult:
    description: str
    score: float


@dataclass
class TextResult:
    text: str
    confidence: float = 0.0


@dataclass
class SafetyResult:
    safe: bool
    categories: Dict[str, Any]


def normalize_labels(items: Any) -> List[Dict[str, Any]]:
    return [{"description": getattr(item, "description", str(item)), "score": float(getattr(item, "score", 0.0))} for item in (items or [])]


def normalize_text_blocks(items: Any) -> List[Dict[str, Any]]:
    normalized = []
    for item in items or []:
        text = getattr(item, "text", None)
        if text is None:
            text = str(item)
        normalized.append({"text": text, "confidence": float(getattr(item, "confidence", 0.0))})
    return normalized
