from dataclasses import dataclass, asdict
from typing import List, Dict


@dataclass
class VisionLabels:
    labels: List[str]


@dataclass
class VisionDescription:
    description: str


@dataclass
class VisionOCR:
    texts: List[str]


@dataclass
class VisionSafety:
    scores: Dict[str, float]


@dataclass
class FullVisionAnalysis:
    labels: VisionLabels
    description: VisionDescription
    ocr: VisionOCR
    safety: VisionSafety
