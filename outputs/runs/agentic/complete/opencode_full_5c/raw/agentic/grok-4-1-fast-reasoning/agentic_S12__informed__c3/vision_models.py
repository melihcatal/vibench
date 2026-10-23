from typing import TypedDict, List, Dict


class ImageLabels(TypedDict):
    labels: List[str]
    confidence_scores: List[float]


class ImageText(TypedDict):
    texts: List[str]


class ImageSafety(TypedDict):
    adult: str
    medical: str
    racy: str
    violence: str


class ImageDescription(TypedDict):
    caption: str
    confidence: float


class VisionAnalysis(TypedDict):
    labels: ImageLabels
    description: ImageDescription
    detected_text: ImageText
    safety: ImageSafety
