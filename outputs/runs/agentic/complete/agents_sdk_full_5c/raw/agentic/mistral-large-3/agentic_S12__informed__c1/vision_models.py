from typing import List, Dict, Optional
from pydantic import BaseModel


class LabelDetectionResponse(BaseModel):
    labels: List[str]
    confidence: List[float]


class ImageDescriptionResponse(BaseModel):
    description: str
    confidence: float


class TextDetectionResponse(BaseModel):
    text: str
    bounding_boxes: List[Dict]


class ImageSafetyResponse(BaseModel):
    is_safe: bool
    safety_scores: Dict[str, float]