from typing import List, Optional, Tuple, Any
from pydantic import BaseModel, Field


class ImageLabel(BaseModel):
    label: str
    confidence: float
    provider: str


class ImageDescription(BaseModel):
    description: str
    provider: str


class ImageText(BaseModel):
    text: str
    confidence: float
    bounding_box: List[Tuple[int, int]]
    provider: str


class ImageSafetyScore(BaseModel):
    label: str
    score: float
    provider: str

class TextSafetyLabel(BaseModel):
    label: str
    confidence: float
    provider: str
    
class TranslatedText(BaseModel):
    text: str
    source_language: str
    target_language: str
    provider: str


class VisualAnalysis(BaseModel):
    source_uri: str
    labels: Optional[List[ImageLabel]] = Field(default_factory=list)
    description: Optional[ImageDescription] = None
    texts: Optional[List[ImageText]] = Field(default_factory=list)
    safety_scores: Optional[List[ImageSafetyScore]] = Field(default_factory=list)
    summary: Optional[str] = None
    translated_description: Optional[TranslatedText] = None
    label_safety_scores: Optional[List[TextSafetyLabel]] = Field(default_factory=list)
    archive_uri: Optional[str] = None
