from dataclasses import dataclass, field
from typing import List


@dataclass
class ImageLabel:
    description: str
    score: float


@dataclass
class ImageDescription:
    text: str


@dataclass
class DetectedText:
    text: str
    confidence: float = 0.0


@dataclass
class SafetyRating:
    category: str
    likelihood: str


@dataclass
class VisionAnalysisResult:
    labels: List[ImageLabel] = field(default_factory=list)
    description: ImageDescription = None
    texts: List[DetectedText] = field(default_factory=list)
    safety_ratings: List[SafetyRating] = field(default_factory=list)
