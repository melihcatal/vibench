from typing import List, Optional
from pydantic import BaseModel


class LabelDetectionResponse(BaseModel):
    provider: str
    labels: List[str]
    confidence: List[float]


class ImageDescriptionResponse(BaseModel):
    provider: str
    description: str


class TextDetectionResponse(BaseModel):
    provider: str
    text: str
    full_text: str


class ImageSafetyResponse(BaseModel):
    provider: str
    adult: str
    violence: str
    racy: str
    medical: str
    spoof: str


class VisualAnalysisSummary(BaseModel):
    labels: List[str]
    description: str
    detected_text: str
    safety_issues: dict