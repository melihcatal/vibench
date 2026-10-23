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
    dominant_colors: List[Dict[str, float]]


class TextDetectionResponse(BaseModel):
    provider: str
    model: str
    detected_text: str
    text_annotations: List[Dict]


class ImageSafetyResponse(BaseModel):
    provider: str
    model: str
    safety_scores: Dict[str, int]


class ImageSummaryRequest(BaseModel):
    labels: List[str]
    description: str
    detected_text: str
    safety_scores: Dict[str, int]


class AltTextTranslateRequest(BaseModel):
    text: str
    target_language: str


class VisualSafetyTextRequest(BaseModel):
    labels: List[str]
    detected_text: str


class ImageAssetArchiveRequest(BaseModel):
    image_path: str
    analysis_results: Dict
    bucket_name: Optional[str] = None
