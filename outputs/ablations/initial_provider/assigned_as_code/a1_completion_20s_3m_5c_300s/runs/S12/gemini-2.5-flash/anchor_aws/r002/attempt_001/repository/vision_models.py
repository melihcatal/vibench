from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ImagePayload(BaseModel):
    image_bytes: bytes = Field(..., description="Image content in bytes")

class LabelResult(BaseModel):
    name: str
    confidence: float

class DetectLabelsResponse(BaseModel):
    labels: List[LabelResult]

class TextDetection(BaseModel):
    detected_text: str
    confidence: float
    bounding_box: Dict[str, Any]

class DetectTextResponse(BaseModel):
    text_detections: List[TextDetection]

class ModerationLabel(BaseModel):
    name: str
    parent_name: Optional[str] = None
    confidence: float

class DetectModerationLabelsResponse(BaseModel):
    moderation_labels: List[ModerationLabel]

class ImageDescriptionResponse(BaseModel):
    description: str

class ImageSummaryRequest(BaseModel):
    detected_labels: List[LabelResult]
    detected_text: Optional[List[TextDetection]] = None
    moderation_labels: Optional[List[ModerationLabel]] = None
    description: Optional[str] = None

class ImageSummaryResponse(BaseModel):
    summary: str

class TranslateTextRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

class TranslateTextResponse(BaseModel):
    translated_text: str

class TextSafetyRequest(BaseModel):
    text: str

class TextSafetyResponse(BaseModel):
    is_unsafe: bool
    safety_details: Dict[str, Any]

class ArchiveAssetRequest(BaseModel):
    image_name: str
    image_bytes: bytes
    analysis_results: Dict[str, Any]
    caption: str

class ArchiveAssetResponse(BaseModel):
    archive_url: str
