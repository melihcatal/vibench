from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ImageSource:
    image_path: Optional[str] = None
    image_bytes: Optional[bytes] = None
    mime_type: str = "image/jpeg"


@dataclass
class LabelDetection:
    name: str
    score: float


@dataclass
class OCRTextBlock:
    text: str
    score: float


@dataclass
class SafetyCategory:
    name: str
    likelihood: str


@dataclass
class VisualDescription:
    text: str
    model: str


@dataclass
class AnalysisSummary:
    labels: List[str] = field(default_factory=list)
    description: str = ""
    detected_text: List[str] = field(default_factory=list)
    safety_flags: List[str] = field(default_factory=list)


def clamp_score(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.0
    if score < 0:
        return 0.0
    if score > 1:
        return 1.0
    return score


def normalize_labels(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in items:
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        normalized.append({"name": name, "score": clamp_score(item.get("score", 0.0))})
    return normalized


def normalize_text_blocks(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in items:
        text = str(item.get("text", "")).strip()
        if not text:
            continue
        normalized.append({"text": text, "score": clamp_score(item.get("score", 0.0))})
    return normalized


def normalize_safety(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in items:
        name = str(item.get("name", "")).strip()
        likelihood = str(item.get("likelihood", "UNKNOWN")).strip().upper() or "UNKNOWN"
        if not name:
            continue
        normalized.append({"name": name, "likelihood": likelihood})
    return normalized
