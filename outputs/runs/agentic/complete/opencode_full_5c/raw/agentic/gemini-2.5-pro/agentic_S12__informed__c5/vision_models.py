from typing import List, Optional
from pydantic import BaseModel


class ImageLabel(BaseModel):
    label: str
    score: float


class ImageLabels(BaseModel):
    labels: List[ImageLabel]


class ImageText(BaseModel):
    text: str
    confidence: float
    bounding_box: Optional[List[dict]] = None


class ImageTexts(BaseModel):
    texts: List[ImageText]


class ImageDescription(BaseModel):
    description: str
    confidence: float


class ImageSafety(BaseModel):
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str


class VisualAnalysis(BaseModel):
    labels: Optional[ImageLabels] = None
    texts: Optional[ImageTexts] = None
    description: Optional[ImageDescription] = None
    safety: Optional[ImageSafety] = None
