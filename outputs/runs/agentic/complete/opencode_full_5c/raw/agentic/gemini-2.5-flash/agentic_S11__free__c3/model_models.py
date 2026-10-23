from typing import Any, Dict, Optional
from pydantic import BaseModel


class PlatformInvocationRequest(BaseModel):
    model_id: str
    prompt: str
    temperature: Optional[float] = 0.7
    max_output_tokens: Optional[int] = 1024


class PlatformInvocationResponse(BaseModel):
    output: str
    model_id: str
    provider: str


class ResourceSelectionRequest(BaseModel):
    model_id: str
    resource_type: str  # e.g., "model", "deployment", "endpoint"


class ResourceSelectionResponse(BaseModel):
    resource_id: str
    resource_type: str
    status: str  # e.g., "available", "unavailable", "error"
    provider: str


class PlatformStreamingResponse(BaseModel):
    chunk: str
    model_id: str
    provider: str
    raw_response_object: Any  # To preserve provider-specific response objects


class PlatformMetadataResponse(BaseModel):
    output: str
    model_id: str
    provider: str
    input_token_count: Optional[int] = None
    output_token_count: Optional[int] = None
    total_token_count: Optional[int] = None
    raw_response_object: Any


class PlatformSafetyCheckRequest(BaseModel):
    text: str
    model_id: str


class PlatformSafetyCheckResponse(BaseModel):
    text: str
    is_safe: bool
    safety_attributes: Optional[Dict[str, Any]] = None
    provider: str


class PlatformTranslationRequest(BaseModel):
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None


class PlatformTranslationResponse(BaseModel):
    translated_text: str
    detected_language_code: Optional[str] = None
    provider: str


class PlatformEmbeddingRequest(BaseModel):
    text: str
    model_id: str


class PlatformEmbeddingResponse(BaseModel):
    embedding: list[float]
    model_id: str
    provider: str


class PlatformAudioBriefingRequest(BaseModel):
    text: str
    voice_name: str
    language_code: str
    audio_encoding: str = "MP3"


class PlatformAudioBriefingResponse(BaseModel):
    audio_content: bytes
    provider: str
