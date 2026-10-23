from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ImageDetectionRequest:
    image_bytes: bytes = field(default=b'')
    image_uri: str = field(default=None)

@dataclass
class LabelDetectionResponse:
    labels: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class TextDetectionResponse:
    text: str = field(default='')

@dataclass
class ImageDescriptionResponse:
    description: str = field(default='')

@dataclass
class SafetyDetectionResponse:
    safe_search_annotations: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TranslationRequest:
    text: str
    target_language: str
    project_id: str

@dataclass
class TranslationResponse:
    translated_text: str

@dataclass
class TextSafetyRequest:
    text: str

@dataclass
class TextSafetyResponse:
    sentiment_score: float
    sentiment_magnitude: float
    categories: List[Dict[str, Any]]

@dataclass
class ArchiveRequest:
    bucket_name: str
    destination_blob_name: str
    data: bytes
