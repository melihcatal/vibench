from typing import List, Tuple
from pydantic import BaseModel

class ImageAnalysisRequest(BaseModel):
    image_path: str

# Label Detection Models
class Label(BaseModel):
    name: str
    confidence: float

class LabelDetectionResponse(BaseModel):
    labels: List[Label]

# Image Description Models
class ImageDescription(BaseModel):
    caption: str
    confidence: float

class DescriptionResponse(BaseModel):
    descriptions: List[ImageDescription]

# Text Detection (OCR) Models
class TextAnnotation(BaseModel):
    text: str
    bounding_box: List[Tuple[int, int]]

class TextDetectionResponse(BaseModel):
    annotations: List[TextAnnotation]

# Image Safety Models
class SafetyLabel(BaseModel):
    name: str
    confidence: float
    parent_name: str

class SafetyResponse(BaseModel):
    safety_labels: List[SafetyLabel]

# Combined Model for Archiving
class FullImageAnalysis(BaseModel):
    labels: LabelDetectionResponse
    description: DescriptionResponse
    text: TextDetectionResponse
    safety: SafetyResponse
