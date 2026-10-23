import os
from typing import List, Optional

from pydantic import BaseModel, Field


class ImageLabel(BaseModel):
    name: str = Field(..., description="The label name.")
    confidence: float = Field(..., description="The confidence score for the label.")


class ImageDescription(BaseModel):
    text: str = Field(..., description="The generated description for the image.")
    confidence: Optional[float] = Field(None, description="The confidence score for the description.")


class DetectedText(BaseModel):
    text: str = Field(..., description="The detected text content.")
    bounding_box: List[int] = Field(..., description="The bounding box coordinates of the text.")
    confidence: float = Field(..., description="The confidence score for the detection.")


class SafetyLabel(BaseModel):
    name: str = Field(..., description="The name of the safety category.")
    confidence: float = Field(..., description="The confidence score for this safety category.")


class ImageSafetyReport(BaseModel):
    safe: bool = Field(..., description="Whether the image is considered safe overall.")
    labels: List[SafetyLabel] = Field(..., description="A list of detected safety-related labels.")


class VisualAnalysis(BaseModel):
    labels: List[ImageLabel] = []
    description: Optional[ImageDescription] = None
    text: List[DetectedText] = []
    safety: Optional[ImageSafetyReport] = None
