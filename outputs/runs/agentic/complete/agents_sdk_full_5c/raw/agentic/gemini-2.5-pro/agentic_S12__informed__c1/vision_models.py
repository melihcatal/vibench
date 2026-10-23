from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ImageLabel:
    name: str
    score: float


@dataclass
class DetectedText:
    text: str
    confidence: float


@dataclass
class SafetyAnnotation:
    category: str
    likelihood: str  # e.g., 'VERY_UNLIKELY', 'LIKELY'


@dataclass
class VisionResult:
    description: Optional[str] = None
    labels: List[ImageLabel] = field(default_factory=list)
    texts: List[DetectedText] = field(default_factory=list)
    safety_annotations: List[SafetyAnnotation] = field(default_factory=list)
