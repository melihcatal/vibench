import base64
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class ImageRequest:
    image_bytes: bytes


@dataclass
class ImageTextDetectionResponse:
    text_annotations: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ImageLabelDetectionResponse:
    labels: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ImageDescriptionResponse:
    description: Optional[str] = None


@dataclass
class ImageSafetyScoreResponse:
    safety_scores: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TextSafetyCheckResponse:
    unsafe_categories: List[str] = field(default_factory=list)


@dataclass
class TranslatedTextResponse:
    translated_text: Optional[str] = None


@dataclass
class SummarizedAnalysisResponse:
    summary: Optional[str] = None


@dataclass
class ArchiveResult:
    archive_url: Optional[str] = None
