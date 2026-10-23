from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Label:
    description: str
    score: float

@dataclass
class TextAnnotation:
    description: str
    bounding_poly: list[tuple[int, int]]

@dataclass
class SafetyAnnotation:
    category: str
    likelihood: str

@dataclass
class ImageDescription:
    text: str
    confidence: float

@dataclass
class FullImageAnalysis:
    labels: list[Label] = field(default_factory=list)
    texts: list[TextAnnotation] = field(default_factory=list)
    safety_scores: list[SafetyAnnotation] = field(default_factory=list)
    description: Optional[ImageDescription] = None
