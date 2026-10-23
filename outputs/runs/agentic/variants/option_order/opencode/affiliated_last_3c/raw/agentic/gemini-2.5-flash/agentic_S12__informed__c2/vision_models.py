from typing import List, Optional
from pydantic import BaseModel


class LatLongRect(BaseModel):
    latitude_north: float
    longitude_west: float
    latitude_south: float
    longitude_east: float


class ImageContext(BaseModel):
    language_hints: Optional[List[str]] = None
    lat_long_rect: Optional[LatLongRect] = None


class DetectedLabelsResponse(BaseModel):
    labels: List[str]


class DescribedImageResponse(BaseModel):
    best_guess_labels: List[str]
    full_matching_images: List[str]


class DetectedTextResponse(BaseModel):
    texts: List[str]
    full_text: str


class ImageSafetyResponse(BaseModel):
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str


class ImageAnalysisResult(BaseModel):
    labels: DetectedLabelsResponse
    description: DescribedImageResponse
    text: DetectedTextResponse
    safety: ImageSafetyResponse


class SummarizedImageAnalysis(BaseModel):
    summary_text: str


class TranslatedText(BaseModel):
    translated_text: str


class TextSafetyCheck(BaseModel):
    unsafe_categories: List[str]
    overall_safety_score: float


class ArchivedAsset(BaseModel):
    asset_url: str
    file_name: str
    content_type: str
