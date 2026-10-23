from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ImageAnalysisRequest:
    image_url: Optional[str] = None
    image_bytes: Optional[bytes] = None


@dataclass
class ImageLabel:
    name: str
    confidence: float


@dataclass
class ImageTextLine:
    text: str
    bounding_box: List[int]


@dataclass
class ImageTextResult:
    lines: List[ImageTextLine]


@dataclass
class ImageDescription:
    text: str
    confidence: float


@dataclass
class ImageSafetyResult:
    category: str
    severity: int
