from typing import List, Dict, Optional
from pydantic import BaseModel


class LabelDetectionResponse(BaseModel):
    labels: List[str]
    confidence: List[float]


class ImageDescriptionResponse(BaseModel):
    description: str


class TextDetectionBlock(BaseModel):
    text: str
    bounding_box: Dict[str, List[Dict[str, int]]]


class TextDetectionResponse(BaseModel):
    text: str
    blocks: List[TextDetectionBlock]


class ImageSafetyResponse(BaseModel):
    adult: str
    violence: str
    racy: str
    medical: str
    spoof: str


class VisualAnalysisSummary(BaseModel):
    labels: List[str]
    description: str
    detected_text: str
    safety_issues: Dict[str, str]


class TranslatedDescriptionResponse(BaseModel):
    original_text: str
    translated_text: str
    target_language: str