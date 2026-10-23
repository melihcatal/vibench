from pydantic import BaseModel, Field
from typing import List, Optional

class ImageLabel(BaseModel):
    label: str = Field(..., description="The detected label or object name.")
    score: float = Field(..., description="The confidence score for the label, from 0 to 1.")

class ImageDescription(BaseModel):
    description: str = Field(..., description="A short textual description of the image.")

class ImageText(BaseModel):
    text: str = Field(..., description="A line of text detected in the image.")
    confidence: float = Field(..., description="The confidence score for the detected text.")

class ImageSafetyScore(BaseModel):
    category: str = Field(..., description="The category of unsafe content (e.g., 'Explicit Nudity').")
    confidence: float = Field(..., description="The confidence score for the safety category.")

class ImageAnalysisResult(BaseModel):
    labels: List[ImageLabel] = Field(..., description="List of detected labels.")
    description: ImageDescription = Field(..., description="Generated image description.")
    detected_texts: List[ImageText] = Field(..., description="List of detected text lines.")
    safety_scores: List[ImageSafetyScore] = Field(..., description="List of safety moderation scores.")
    source_image_path: str = Field(..., description="The local path of the analyzed image.")

class TranslatedText(BaseModel):
    original_text: str
    translated_text: str
    target_language: str

class TextSafetyResult(BaseModel):
    is_safe: bool
    flagged_categories: dict[str, bool]

class ArchiveResult(BaseModel):
    image_url: str
    metadata_url: str
    container_name: str
