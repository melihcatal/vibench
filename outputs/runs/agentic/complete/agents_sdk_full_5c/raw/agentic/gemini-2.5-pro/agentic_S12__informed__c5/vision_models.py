"""
[HELPER] vision_models.py - Define local request, response, and normalization helpers for Static Image and Visual Understanding
"""
from typing import List, Optional, Tuple
from pydantic import BaseModel

class Label(BaseModel):
    name: str
    confidence: float

class TextDetection(BaseModel):
    text: str
    confidence: float
    box: Tuple[float, float, float, float]  # Left, Top, Width, Height

class ModerationLabel(BaseModel):
    name: str
    confidence: float

class VisionResult(BaseModel):
    labels: Optional[List[Label]] = None
    text_detections: Optional[List[TextDetection]] = None
    moderation_labels: Optional[List[ModerationLabel]] = None
    description: Optional[str] = None
