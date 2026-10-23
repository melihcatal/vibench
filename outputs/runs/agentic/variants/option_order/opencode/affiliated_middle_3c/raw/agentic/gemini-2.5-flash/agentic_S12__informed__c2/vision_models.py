import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class ImageRequest:
    image_content: Optional[bytes] = None
    image_uri: Optional[str] = None


@dataclasses.dataclass
class LabelDetectionResult:
    description: str
    score: float


@dataclasses.dataclass
class TextDetectionResult:
    text: str
    bounds: List[float]  # Bounding box vertices (flat list of x, y coordinates)


@dataclasses.dataclass
class SafeSearchDetectionResult:
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str


@dataclasses.dataclass
class VisionResponse:
    labels: List[LabelDetectionResult] = dataclasses.field(default_factory=list)
    text_annotations: List[TextDetectionResult] = dataclasses.field(
        default_factory=list
    )
    safe_search_annotation: Optional[SafeSearchDetectionResult] = None
    full_text_annotation: Optional[str] = None
