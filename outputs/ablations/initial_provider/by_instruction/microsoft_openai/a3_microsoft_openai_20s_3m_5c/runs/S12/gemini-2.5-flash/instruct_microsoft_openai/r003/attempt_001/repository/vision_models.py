from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ImageRequest:
    image_url: Optional[str] = None
    image_content: Optional[bytes] = None
    image_uri: Optional[str] = None

@dataclass
class LabelDetectionResult:
    description: str
    score: float

@dataclass
class ImageLabelResponse:
    labels: List[LabelDetectionResult] = field(default_factory=list)

@dataclass
class ImageDescriptionResponse:
    description: str

@dataclass
class ImageTextResponse:
    text: str

@dataclass
class ImageSafetyResponse:
    explicit_content_likelihood: str
