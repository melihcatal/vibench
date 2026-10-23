from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional


@dataclass
class ImageRequest:
    image_path: str
    max_labels: int = 10
    language: str = "en"
    detail: str = "short"


@dataclass
class VisionLabel:
    name: str
    confidence: float


@dataclass
class VisionDescription:
    text: str
    confidence: Optional[float] = None


@dataclass
class VisionTextBlock:
    text: str
    confidence: Optional[float] = None


@dataclass
class VisionSafetyFinding:
    category: str
    severity: str
    score: Optional[float] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedVisionResult:
    labels: List[VisionLabel] = field(default_factory=list)
    description: Optional[VisionDescription] = None
    text_blocks: List[VisionTextBlock] = field(default_factory=list)
    safety_findings: List[VisionSafetyFinding] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def clamp_text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def normalize_labels(items: Iterable[Mapping[str, Any]]) -> List[VisionLabel]:
    normalized: List[VisionLabel] = []
    for item in items:
        name = clamp_text(item.get("name") or item.get("Description") or item.get("label"))
        confidence = item.get("confidence") or item.get("Confidence") or item.get("score") or 0.0
        try:
            confidence_f = float(confidence)
        except (TypeError, ValueError):
            confidence_f = 0.0
        if name:
            normalized.append(VisionLabel(name=name, confidence=confidence_f))
    return normalized


def normalize_text_blocks(items: Iterable[Mapping[str, Any]]) -> List[VisionTextBlock]:
    blocks: List[VisionTextBlock] = []
    for item in items:
        text = clamp_text(item.get("text") or item.get("DetectedText") or item.get("value"))
        confidence = item.get("confidence") or item.get("Confidence") or item.get("score")
        try:
            conf = None if confidence is None else float(confidence)
        except (TypeError, ValueError):
            conf = None
        if text:
            blocks.append(VisionTextBlock(text=text, confidence=conf))
    return blocks


def normalize_safety_findings(items: Iterable[Mapping[str, Any]]) -> List[VisionSafetyFinding]:
    findings: List[VisionSafetyFinding] = []
    for item in items:
        category = clamp_text(item.get("category") or item.get("Category") or item.get("name"))
        severity = clamp_text(item.get("severity") or item.get("Severity") or item.get("level") or "unknown")
        score = item.get("score") or item.get("confidence") or item.get("Confidence")
        try:
            score_f = None if score is None else float(score)
        except (TypeError, ValueError):
            score_f = None
        details = dict(item)
        if category:
            findings.append(VisionSafetyFinding(category=category, severity=severity, score=score_f, details=details))
    return findings
