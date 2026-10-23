from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ImageInput:
    image_path: Optional[str] = None
    image_url: Optional[str] = None
    mime_type: str = "image/jpeg"


@dataclass
class LabelResult:
    name: str
    score: float


@dataclass
class TextBlock:
    text: str
    score: float = 0.0


@dataclass
class SafetyRating:
    category: str
    probability: str
    blocked: bool = False


@dataclass
class VisionAnalysis:
    labels: List[LabelResult] = field(default_factory=list)
    description: str = ""
    texts: List[TextBlock] = field(default_factory=list)
    safety: List[SafetyRating] = field(default_factory=list)
    source: Dict[str, Any] = field(default_factory=dict)


def normalize_labels(items: List[Dict[str, Any]]) -> List[LabelResult]:
    normalized: List[LabelResult] = []
    for item in items or []:
        name = str(item.get("name") or item.get("description") or "").strip()
        if not name:
            continue
        score = float(item.get("score") or item.get("confidence") or 0.0)
        normalized.append(LabelResult(name=name, score=score))
    return normalized


def normalize_texts(items: List[Dict[str, Any]]) -> List[TextBlock]:
    normalized: List[TextBlock] = []
    for item in items or []:
        text = str(item.get("text") or item.get("description") or "").strip()
        if not text:
            continue
        score = float(item.get("score") or item.get("confidence") or 0.0)
        normalized.append(TextBlock(text=text, score=score))
    return normalized


def normalize_safety(items: List[Dict[str, Any]]) -> List[SafetyRating]:
    normalized: List[SafetyRating] = []
    for item in items or []:
        category = str(item.get("category") or item.get("name") or "").strip()
        probability = str(
            item.get("probability") or item.get("likelihood") or "UNKNOWN"
        ).strip()
        blocked = bool(item.get("blocked") or False)
        if category:
            normalized.append(
                SafetyRating(
                    category=category, probability=probability, blocked=blocked
                )
            )
    return normalized


def analysis_to_dict(analysis: VisionAnalysis) -> Dict[str, Any]:
    return {
        "labels": [
            {"name": item.name, "score": item.score} for item in analysis.labels
        ],
        "description": analysis.description,
        "texts": [{"text": item.text, "score": item.score} for item in analysis.texts],
        "safety": [
            {
                "category": item.category,
                "probability": item.probability,
                "blocked": item.blocked,
            }
            for item in analysis.safety
        ],
        "source": analysis.source,
    }
