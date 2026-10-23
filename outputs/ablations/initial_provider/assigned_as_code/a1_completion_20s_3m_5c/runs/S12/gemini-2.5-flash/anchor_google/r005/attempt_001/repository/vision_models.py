import dataclasses
from typing import List, Dict, Any

@dataclasses.dataclass
class VisionRequest:
    image_bytes: bytes
    mime_type: str = "image/jpeg" # Default to JPEG, can be overridden

@dataclasses.dataclass
class Label:
    name: str
    confidence: float

@dataclasses.dataclass
class DetectedText:
    text: str
    bounds: List[Dict[str, Any]]

@dataclasses.dataclass
class ImageProperties:
    colors: List[Dict[str, Any]]

@dataclasses.dataclass
class SafeSearchAnnotation:
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str

@dataclasses.dataclass
class WebDetection:
    full_matching_images: List[Dict[str, Any]]
    partial_matching_images: List[Dict[str, Any]]
    web_entities: List[Dict[str, Any]]

@dataclasses.dataclass
class ImageContext:
    lat_long_rect: Dict[str, Any] = None
    language_hints: List[str] = None

@dataclasses.dataclass
class ImageResponse:
    labels: List[Label] = dataclasses.field(default_factory=list)
    text_annotations: List[DetectedText] = dataclasses.field(default_factory=list)
    full_text_annotation: Dict[str, Any] = dataclasses.field(default_factory=dict)
    safe_search_annotation: SafeSearchAnnotation = None
    localized_object_annotations: List[Dict[str, Any]] = dataclasses.field(default_factory=list)
    web_detection: WebDetection = None
    image_properties: ImageProperties = None
    error: Dict[str, Any] = dataclasses.field(default_factory=dict)
    description: str = None # For image description results
