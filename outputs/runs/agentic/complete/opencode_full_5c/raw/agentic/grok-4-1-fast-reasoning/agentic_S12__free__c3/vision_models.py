from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class ImageLabels:
    labels: List[str]


@dataclass
class ImageDescription:
    description: str


@dataclass
class DetectedText:
    text: str


@dataclass
class SafetyScore:
    score: float
    categories: Dict[str, float]


@dataclass
class FullVisionAnalysis:
    labels: ImageLabels
    description: ImageDescription
    text: DetectedText
    safety: SafetyScore
