import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class ImageDetectionRequest:
    image_uri: str


@dataclasses.dataclass
class Label:
    description: str
    score: float


@dataclasses.dataclass
class ImageLabelDetectionResponse:
    labels: List[Label]


@dataclasses.dataclass
class TextAnnotation:
    description: str
    bounds: List[List[int]]


@dataclasses.dataclass
class ImageTextDetectionResponse:
    text_annotations: List[TextAnnotation]


@dataclasses.dataclass
class SafeSearchAnnotation:
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str


@dataclasses.dataclass
class ImageSafetyDetectionResponse:
    safe_search_annotation: SafeSearchAnnotation


@dataclasses.dataclass
class ImageDescriptionResponse:
    description: str


@dataclasses.dataclass
class ImageSummaryRequest:
    labels: List[str]
    description: str
    detected_text: str
    safety_scores: dict


@dataclasses.dataclass
class ImageSummaryResponse:
    summary: str


@dataclasses.dataclass
class AltTextTranslateRequest:
    text: str
    target_language: str


@dataclasses.dataclass
class AltTextTranslateResponse:
    translated_text: str


@dataclasses.dataclass
class VisualSafetyTextRequest:
    text: str


@dataclasses.dataclass
class VisualSafetyTextResponse:
    is_safe: bool
    scores: dict


@dataclasses.dataclass
class ImageAssetArchiveRequest:
    image_uri: str
    labels: List[str]
    description: str
    summary: str
    translated_text: str
    safety_scores: dict
    text_safety_scores: dict


@dataclasses.dataclass
class ImageAssetArchiveResponse:
    archive_url: str
