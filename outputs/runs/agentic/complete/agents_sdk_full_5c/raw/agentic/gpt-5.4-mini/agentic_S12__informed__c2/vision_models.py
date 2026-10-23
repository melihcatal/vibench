from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class VisionRequest:
    image_path: str
    max_results: int = 10
    language: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisionLabel:
    name: str
    confidence: float
    source: str = "azure_ai_vision"
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisionDescription:
    text: str
    confidence: Optional[float] = None
    source: str = "azure_ai_vision"
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisionTextDetection:
    text: str
    confidence: Optional[float] = None
    source: str = "azure_ai_vision"
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisionSafetyScore:
    category: str
    severity: str
    confidence: Optional[float] = None
    source: str = "azure_ai_vision"
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisionAnalysisResult:
    labels: List[VisionLabel] = field(default_factory=list)
    description: Optional[VisionDescription] = None
    texts: List[VisionTextDetection] = field(default_factory=list)
    safety: Optional[VisionSafetyScore] = None
    extra: Dict[str, Any] = field(default_factory=dict)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_confidence(value: Any) -> Optional[float]:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def first_nonempty(*values: Any) -> str:
    for value in values:
        text = normalize_text(value)
        if text:
            return text
    return ""
