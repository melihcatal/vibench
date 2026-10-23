from pydantic import BaseModel, Field
from typing import List

class ImageLabel(BaseModel):
    name: str = Field(..., description="The detected label or object name.")
    confidence: float = Field(..., description="The confidence score for the label.")

class ImageDescription(BaseModel):
    text: str = Field(..., description="A short visual description of the image.")

class DetectedText(BaseModel):
    text: str = Field(..., description="The detected text content.")
    confidence: float = Field(..., description="The confidence score for the detected text.")
    bounding_box: List[int] = Field(..., description="Coordinates of the bounding box for the text.")

class SafetyAnnotation(BaseModel):
    category: str = Field(..., description="The category of unsafe content (e.g., 'adult', 'violence').")
    likelihood: str = Field(..., description="Likelihood of the content belonging to the category.")

class FullImageAnalysis(BaseModel):
    labels: List[ImageLabel]
    description: ImageDescription
    texts: List[DetectedText]
    safety_scores: List[SafetyAnnotation]

class AnalysisSummary(BaseModel):
    summary_text: str

class TranslatedText(BaseModel):
    text: str
    source_lang: str
    target_lang: str

class TextSafetyScore(BaseModel):
    attribute: str = Field(..., description="The safety attribute being scored (e.g., 'TOXICITY').")
    score: float = Field(..., description="The score for the attribute.")

class ArchiveResult(BaseModel):
    bucket: str
    key: str
    url: str
