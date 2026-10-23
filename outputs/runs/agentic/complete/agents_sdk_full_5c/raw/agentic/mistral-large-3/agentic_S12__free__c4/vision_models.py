from typing import List, Dict, Optional
from pydantic import BaseModel


class LabelDetectionResponse(BaseModel):
    labels: List[str]
    confidence: List[float]


class ImageDescriptionResponse(BaseModel):
    description: str


class TextDetectionResponse(BaseModel):
    full_text: str
    text_annotations: List[str]


class SafetyRatingResponse(BaseModel):
    safety_ratings: Dict[str, int]


class VisualAnalysisSummary(BaseModel):
    labels: Optional[List[str]] = None
    description: Optional[str] = None
    detected_text: Optional[str] = None
    safety_ratings: Optional[Dict[str, int]] = None