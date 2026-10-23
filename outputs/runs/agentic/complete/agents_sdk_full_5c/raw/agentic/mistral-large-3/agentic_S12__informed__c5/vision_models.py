from typing import List, Optional
from pydantic import BaseModel

class LabelDetectionResponse(BaseModel):
    labels: List[str]
    confidences: List[float]

class ImageDescriptionResponse(BaseModel):
    description: str

class TextDetectionResponse(BaseModel):
    texts: List[str]

class ImageSafetyResponse(BaseModel):
    is_safe: bool
    unsafe_concepts: List[str]