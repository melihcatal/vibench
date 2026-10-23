from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class ImageRequest:
    source: str


@dataclass
class LabelItem:
    name: str
    score: float


@dataclass
class TextBlock:
    text: str
    score: float = 0.0


@dataclass
class SafetyFinding:
    category: str
    score: float
    flagged: bool


@dataclass
class NormalizedVisionResult:
    labels: List[LabelItem]
    description: str
    text: List[TextBlock]
    safety: List[SafetyFinding]


def normalize_label(annotation: Any) -> Dict[str, Any]:
    return {"name": getattr(annotation, "description", ""), "score": float(getattr(annotation, "score", 0.0) or 0.0)}


def normalize_text(annotation: Any) -> Dict[str, Any]:
    return {"text": getattr(annotation, "description", ""), "score": float(getattr(annotation, "score", 0.0) or 0.0)}


def normalize_safety(name: str, likelihood: Any) -> Dict[str, Any]:
    score = float(getattr(likelihood, "value", likelihood) if likelihood is not None else 0.0)
    return {"category": name, "score": score, "flagged": score >= 3.0}
