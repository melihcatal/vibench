from typing import List, Optional
from pydantic import BaseModel


class ImageLabel(BaseModel):
    name: str
    confidence: float


class ImageDescription(BaseModel):
    text: str
    confidence: float


class BoundingBox(BaseModel):
    x_min: int
    y_min: int
    x_max: int
    y_max: int


class ImageText(BaseModel):
    text: str
    bounding_box: BoundingBox


class ImageSafetyScore(BaseModel):
    category: str
    probability: float


class VisualAnalysis(BaseModel):
    labels: Optional[List[ImageLabel]] = None
    description: Optional[ImageDescription] = None
    text: Optional[List[ImageText]] = None
    safety_scores: Optional[List[ImageSafetyScore]] = None
