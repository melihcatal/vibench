from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List

class PlatformInvocationRequest(BaseModel):
    text: str
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=500, ge=1)

class PlatformInvocationResponse(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None

class StreamingPlatformInvocationResponse(BaseModel):
    chunk: str
    metadata: Optional[Dict[str, Any]] = None

class PlatformSafetyCheckRequest(BaseModel):
    text: str

class PlatformSafetyCheckResponse(BaseModel):
    is_safe: bool
    reasons: List[str]

class PlatformLocalizationRequest(BaseModel):
    text: str
    target_language: str

class PlatformLocalizationResponse(BaseModel):
    translated_text: str

class PlatformEmbeddingRequest(BaseModel):
    text: str

class PlatformEmbeddingResponse(BaseModel):
    embedding: List[float]

class PlatformAudioBriefRequest(BaseModel):
    text: str
    language_code: str = "en-US"
    voice_name: str = "en-US-Neural2-C"

class PlatformAudioBriefResponse(BaseModel):
    audio_content: str # Base64 encoded audio content
