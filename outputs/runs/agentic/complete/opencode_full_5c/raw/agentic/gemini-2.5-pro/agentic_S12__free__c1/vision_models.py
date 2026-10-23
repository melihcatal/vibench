from typing import List, Optional
from pydantic import BaseModel, Field


class Label(BaseModel):
    description: str
    score: float


class TextAnnotation(BaseModel):
    description: str
    bounding_poly: List[dict]


class SafeSearchAnnotation(BaseModel):
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str


class ImageDescription(BaseModel):
    text: str


class VisualAnalysis(BaseModel):
    labels: Optional[List[Label]] = Field(default_factory=list)
    texts: Optional[List[TextAnnotation]] = Field(default_factory=list)
    safe_search: Optional[SafeSearchAnnotation] = None
    description: Optional[ImageDescription] = None


class TextSafetyResult(BaseModel):
    is_safe: bool
    flagged_categories: List[str] = Field(default_factory=list)
