from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ImageClassification:
    label: str
    score: float


@dataclass
class ImageDescription:
    text: str


@dataclass
class ImageText:
    text: str
    bounding_box: list


@dataclass
class ImageSafety:
    category: str
    severity: str
    score: float


@dataclass
class VisionRequest:
    image_uri: str


@dataclass
class VisionResponse:
    labels: Optional[List[ImageClassification]] = None
    descriptions: Optional[List[ImageDescription]] = None
    texts: Optional[List[ImageText]] = None
    safety_scores: Optional[List[ImageSafety]] = None


@dataclass
class SummaryRequest:
    labels: List[ImageClassification]
    descriptions: List[ImageDescription]
    texts: List[ImageText]
    safety_scores: List[ImageSafety]


@dataclass
class SummaryResponse:
    summary: str


@dataclass
class TranslationRequest:
    text: str
    target_language: str


@dataclass
class TranslationResponse:
    translated_text: str


@dataclass
class TextSafetyRequest:
    text: str


@dataclass
class TextSafetyResponse:
    scores: dict


@dataclass
class ArchiveRequest:
    image_uri: str
    analysis_results: dict
    caption: str
