from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Feature:
    type: str  # e.g., 'LABEL_DETECTION', 'TEXT_DETECTION', 'SAFE_SEARCH_DETECTION'
    max_results: Optional[int] = None


@dataclass
class ImageSource:
    image_uri: Optional[str] = None


@dataclass
class Image:
    content: Optional[bytes] = None
    source: Optional[ImageSource] = None


@dataclass
class AnnotateImageRequest:
    image: Image
    features: List[Feature]


@dataclass
class LabelAnnotation:
    mid: str
    description: str
    score: float
    topicality_score: float


@dataclass
class TextAnnotation:
    description: str
    locale: Optional[str] = None


@dataclass
class SafeSearchAnnotation:
    adult: str
    racy: str
    medical: str
    violence: str
    spoof: str


@dataclass
class ImageDescription:
    labels: List[str] = field(default_factory=list)
    text: Optional[str] = None
