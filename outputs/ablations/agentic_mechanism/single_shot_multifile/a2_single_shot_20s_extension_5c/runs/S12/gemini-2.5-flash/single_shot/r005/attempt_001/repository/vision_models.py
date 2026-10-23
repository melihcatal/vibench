from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class ImageInput:
    image_bytes: Optional[bytes] = None
    image_url: Optional[str] = None

    def __post_init__(self):
        if not (self.image_bytes or self.image_url):
            raise ValueError("Either image_bytes or image_url must be provided.")

@dataclass
class LabelResult:
    description: str
    score: float
    category: Optional[str] = None

@dataclass
class TextDetectionResult:
    text: str
    bounding_box: Optional[Dict[str, Any]] = None

@dataclass
class SafeSearchResult:
    category: str
    likelihood: str

@dataclass
class ImageDescriptionResult:
    caption: str
    confidence: Optional[float] = None

@dataclass
class VisionAnalysisResults:
    image_input: ImageInput
    labels: List[LabelResult] = field(default_factory=list)
    description: Optional[ImageDescriptionResult] = None
    detected_text: List[TextDetectionResult] = field(default_factory=list)
    safety_scores: Dict[str, SafeSearchResult] = field(default_factory=dict)

@dataclass
class SummaryInput:
    labels: List[str]
    description: str
    detected_text_snippets: List[str]
    safety_warnings: List[str]

@dataclass
class TranslatedText:
    text: str
    language_code: str

@dataclass
class ModerationResult:
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]

@dataclass
class ArchiveItem:
    filename: str
    content: bytes
    content_type: str