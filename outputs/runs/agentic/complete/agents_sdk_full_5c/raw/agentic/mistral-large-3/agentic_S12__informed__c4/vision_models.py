from typing import List, Dict, Optional
from pydantic import BaseModel


class LabelDetectionResponse(BaseModel):
    labels: List[str]
    confidence: List[float]


class ImageDescriptionResponse(BaseModel):
    description: str
    confidence: float


class TextBlock(BaseModel):
    text: str
    bounding_box: Dict[str, List[Dict[str, int]]]


class TextDetectionResponse(BaseModel):
    full_text: str
    blocks: List[TextBlock]


class ImageSafetyResponse(BaseModel):
    is_safe: bool
    safety_ratings: Dict[str, int]