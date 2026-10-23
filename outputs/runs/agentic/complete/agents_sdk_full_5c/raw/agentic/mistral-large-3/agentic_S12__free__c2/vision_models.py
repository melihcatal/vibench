from typing import List, Dict, Optional
from pydantic import BaseModel

class LabelDetectionResponse(BaseModel):
    provider: str
    labels: List[str]
    confidence: List[float]

class ImageDescriptionResponse(BaseModel):
    provider: str
    description: str

class TextDetectionResponse(BaseModel):
    provider: str
    text: str
    bounding_boxes: List[Dict]

class ImageSafetyResponse(BaseModel):
    provider: str
    safety_scores: Dict[str, int]

class VisualAnalysisSummary(BaseModel):
    labels: Optional[LabelDetectionResponse] = None
    description: Optional[ImageDescriptionResponse] = None
    text: Optional[TextDetectionResponse] = None
    safety: Optional[ImageSafetyResponse] = None