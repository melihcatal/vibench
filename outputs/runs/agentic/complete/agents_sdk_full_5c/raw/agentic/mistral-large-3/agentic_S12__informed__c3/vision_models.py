from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class LabelDetectionResponse(BaseModel):
    provider: str
    labels: List[str]
    raw_response: Any

class ImageDescriptionResponse(BaseModel):
    provider: str
    description: str
    raw_response: Any

class TextDetectionResponse(BaseModel):
    provider: str
    texts: List[str]
    raw_response: Any

class ImageSafetyResponse(BaseModel):
    provider: str
    safety_scores: Dict[str, float]
    raw_response: Any

class VisualAnalysisSummary(BaseModel):
    labels: Optional[List[str]] = None
    description: Optional[str] = None
    texts: Optional[List[str]] = None
    safety_scores: Optional[Dict[str, float]] = None