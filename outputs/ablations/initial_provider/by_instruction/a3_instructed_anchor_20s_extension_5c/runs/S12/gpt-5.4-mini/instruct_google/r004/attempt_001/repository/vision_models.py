from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class VisionImageInput:
    image_path: Optional[str] = None
    image_bytes: Optional[bytes] = None
    mime_type: str = "image/jpeg"


@dataclass
class VisionLabel:
    name: str
    score: float = 0.0


@dataclass
class VisionTextBlock:
    text: str
    score: float = 0.0


@dataclass
class VisionSafetyFinding:
    category: str
    likelihood: str
    confidence: float = 0.0


@dataclass
class VisionAnalysisResult:
    provider: str
    kind: str
    raw: Dict[str, Any] = field(default_factory=dict)
    labels: List[VisionLabel] = field(default_factory=list)
    text: List[VisionTextBlock] = field(default_factory=list)
    safety: List[VisionSafetyFinding] = field(default_factory=list)
    description: str = ""


def normalize_labels(items: Any) -> List[VisionLabel]:
    normalized: List[VisionLabel] = []
    for item in items or []:
        if isinstance(item, dict):
            normalized.append(VisionLabel(name=str(item.get("name", item.get("description", ""))), score=float(item.get("score", item.get("confidence", 0.0)) or 0.0)))
        else:
            normalized.append(VisionLabel(name=str(item), score=0.0))
    return normalized


def normalize_text(items: Any) -> List[VisionTextBlock]:
    normalized: List[VisionTextBlock] = []
    for item in items or []:
        if isinstance(item, dict):
            normalized.append(VisionTextBlock(text=str(item.get("text", item.get("description", ""))), score=float(item.get("score", item.get("confidence", 0.0)) or 0.0)))
        else:
            normalized.append(VisionTextBlock(text=str(item), score=0.0))
    return normalized


def normalize_safety(items: Any) -> List[VisionSafetyFinding]:
    normalized: List[VisionSafetyFinding] = []
    for item in items or []:
        if isinstance(item, dict):
            normalized.append(VisionSafetyFinding(category=str(item.get("category", item.get("name", ""))), likelihood=str(item.get("likelihood", item.get("severity", "UNKNOWN"))), confidence=float(item.get("confidence", item.get("score", 0.0)) or 0.0)))
    return normalized
