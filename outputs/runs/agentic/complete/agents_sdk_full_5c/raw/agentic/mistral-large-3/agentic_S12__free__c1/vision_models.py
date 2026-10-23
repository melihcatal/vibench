from typing import List, Dict, Optional
from pydantic import BaseModel


class LabelDetectionResponse(BaseModel):
    provider: str
    labels: List[str]
    confidence_scores: List[float]


class ImageDescriptionResponse(BaseModel):
    provider: str
    description: str


class TextDetectionResponse(BaseModel):
    provider: str
    text: str
    bounding_polygons: List[Dict]


class ImageSafetyResponse(BaseModel):
    provider: str
    safety_scores: Dict[str, int]


class VisualAnalysisSummary(BaseModel):
    labels: List[str]
    description: str
    detected_text: str
    safety_scores: Dict[str, int]


class TranslationRequest(BaseModel):
    text: str
    target_language: str


class TranslationResponse(BaseModel):
    provider: str
    translated_text: str


class SafetyTextResponse(BaseModel):
    provider: str
    is_unsafe: bool
    unsafe_categories: List[str]


class ArchiveRequest(BaseModel):
    image_path: str
    analysis_results: Dict
    destination_blob_name: str