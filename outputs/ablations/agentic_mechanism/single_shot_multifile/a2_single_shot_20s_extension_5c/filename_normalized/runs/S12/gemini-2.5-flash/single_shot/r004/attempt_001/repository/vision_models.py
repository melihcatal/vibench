from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ImageInput(BaseModel):
    content_base64: Optional[str] = Field(None, description="Base64 encoded image content.")
    image_uri: Optional[str] = Field(None, description="Publicly accessible URL, GCS URI (gs://), or S3 URI (s3://) of the image.")

    class Config:
        extra = 'forbid'

class LabelDetectionResult(BaseModel):
    labels: List[Dict[str, Any]] = Field(..., description="List of detected labels with their confidence scores.")

class ImageDescriptionResult(BaseModel):
    description: str = Field(..., description="A concise visual description of the image.")

class TextDetectionResult(BaseModel):
    full_text: str = Field(..., description="The full text detected in the image.")
    detected_texts: List[Dict[str, Any]] = Field(..., description="List of individual text segments with their bounding boxes.")

class SafetyScoreResult(BaseModel):
    safety_scores: Dict[str, Any] = Field(..., description="Safety scores for different content categories (e.g., adult, racy, gore).")

class ImageSummaryRequest(BaseModel):
    image_labels: LabelDetectionResult
    image_description: ImageDescriptionResult
    detected_text: TextDetectionResult
    safety_scores: SafetyScoreResult

class ImageSummaryResult(BaseModel):
    summary_text: str = Field(..., description="A summary of the visual analysis results.")

class TranslationRequest(BaseModel):
    text: str
    target_language_code: str

class TranslationResult(BaseModel):
    translated_text: str
    source_language_code: str

class TextSafetyRequest(BaseModel):
    texts: List[str]

class TextSafetyResult(BaseModel):
    moderation_results: List[Dict[str, Any]]

class ArchiveRequest(BaseModel):
    filename: str
    content_base64: Optional[str] = None
    text_content: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

class ArchiveResult(BaseModel):
    archive_url: str
    message: str
