from typing import List, Dict, Optional
from pydantic import BaseModel


class LabelDetectionResponse(BaseModel):
    provider: str
    model: str
    labels: List[str]
    confidence_scores: List[float]


class ImageDescriptionResponse(BaseModel):
    provider: str
    model: str
    description: str


class TextDetectionResponse(BaseModel):
    provider: str
    model: str
    texts: List[str]


class SafetyRatingResponse(BaseModel):
    provider: str
    model: str
    ratings: Dict[str, int]


class ImageSummaryRequest(BaseModel):
    labels: List[str]
    description: str
    texts: List[str]
    safety_ratings: Dict[str, int]


class AltTextTranslationRequest(BaseModel):
    description: str
    target_language: str


class VisualSafetyTextRequest(BaseModel):
    texts: List[str]


class ArchiveRequest(BaseModel):
    image_path: str
    analysis_results: Dict
