from pydantic import BaseModel, Field
from typing import List, Optional


class LabelAnnotation(BaseModel):
    mid: str
    description: str
    score: float
    topicality: float


class LocalizedObjectAnnotation(BaseModel):
    mid: str
    name: str
    score: float


class TextAnnotation(BaseModel):
    description: str
    locale: Optional[str] = None


class SafeSearchAnnotation(BaseModel):
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str


class VisionAPIResponse(BaseModel):
    label_annotations: List[LabelAnnotation] = Field(default_factory=list)
    localized_object_annotations: List[LocalizedObjectAnnotation] = Field(
        default_factory=list
    )
    text_annotations: List[TextAnnotation] = Field(default_factory=list)
    safe_search_annotation: Optional[SafeSearchAnnotation] = None
