from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class ImageLabel(BaseModel):
    label: str
    score: float

class DetectedText(BaseModel):
    text: str
    confidence: float
    geometry: Dict

class ImageSafetyScore(BaseModel):
    category: str
    confidence: float

class VisualAnalysis(BaseModel):
    """
    A comprehensive model to hold all visual analysis results for a single image.
    """
    image_uri: str
    description: Optional[str] = Field(None, description="A generated visual description of the image.")
    labels: List[ImageLabel] = Field(default_factory=list, description="List of detected labels or objects.")
    detected_texts: List[DetectedText] = Field(default_factory=list, description="List of text blocks found in the image.")
    safety_scores: List[ImageSafetyScore] = Field(default_factory=list, description="List of content safety moderation labels.")
    
class TextSafetyAnalysis(BaseModel):
    """
    Model for storing text safety analysis results.
    """
    text: str
    is_toxic: bool
    toxicity_score: float

class Translation(BaseModel):
    """
    Model for storing translation results.
    """
    source_text: str
    translated_text: str
    target_language: str
