from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ImageLabel:
    description: str
    score: float


@dataclass
class ImageText:
    description: str
    bounding_poly: list


@dataclass
class ImageSafety:
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str


@dataclass
class VisionAnalysis:
    labels: List[ImageLabel]
    texts: List[ImageText]
    safety: Optional[ImageSafety]
    description: Optional[str]
