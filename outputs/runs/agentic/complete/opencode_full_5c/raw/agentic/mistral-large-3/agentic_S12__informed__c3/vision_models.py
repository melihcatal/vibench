from typing import List, Dict, Optional
from pydantic import BaseModel


class LabelDetectionResponse(BaseModel):
    labels: List[str]
    confidence: List[float]


class TextDetectionResponse(BaseModel):
    text: str
    bounding_boxes: List[Dict]


class ImageDescriptionResponse(BaseModel):
    description: str
    dominant_colors: List[Dict]


class SafetyRatingResponse(BaseModel):
    adult: int
    violence: int
    racy: int
    medical: int
    spoof: int


class ImageAnalysisSummary(BaseModel):
    labels: Optional[LabelDetectionResponse] = None
    text: Optional[TextDetectionResponse] = None
    description: Optional[ImageDescriptionResponse] = None
    safety_ratings: Optional[SafetyRatingResponse] = None


class TranslatedTextResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str


class SafetyTextResponse(BaseModel):
    is_safe: bool
    unsafe_categories: List[str]
    confidence: float
