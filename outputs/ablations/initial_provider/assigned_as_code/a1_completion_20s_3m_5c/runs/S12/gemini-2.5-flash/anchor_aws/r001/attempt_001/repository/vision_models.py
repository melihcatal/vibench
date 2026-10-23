from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class ImagePayload:
    image_bytes: bytes


@dataclass
class LabelResult:
    name: str
    confidence: float


@dataclass
class LabelsResponse:
    labels: List[LabelResult]


@dataclass
class DescriptionResponse:
    description: str


@dataclass
class TextDetectionResult:
    text: str
    confidence: float
    type: str
    bounding_box: Dict[str, float]


@dataclass
class TextDetectionResponse:
    text_detections: List[TextDetectionResult]


@dataclass
class ModerationLabel:
    name: str
    confidence: float


@dataclass
class SafetyScoreResponse:
    moderation_labels: List[ModerationLabel]


@dataclass
class SummaryRequest:
    analysis_results: Dict[str, Any]


@dataclass
class SummaryResponse:
    summary: str


@dataclass
class TranslationRequest:
    text: str
    source_language_code: str
    target_language_code: str


@dataclass
class TranslationResponse:
    translated_text: str


@dataclass
class TextSafetyRequest:
    text_content: str


@dataclass
class TextSafetyResponse:
    is_unsafe: bool
    safety_details: str


@dataclass
class ArchiveRequest:
    bucket_name: str
    file_name: str
    content: bytes
    metadata: Optional[Dict[str, str]] = None


@dataclass
class ArchiveResponse:
    object_url: str